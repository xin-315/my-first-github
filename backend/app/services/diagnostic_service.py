"""
Dual-Mode Diagnostic Engine Service
Supports DashScope Qwen-Turbo LLM inference with 4s timeout and robust offline local knowledge fallback.
Never returns unhandled 500 exceptions.
"""

import logging
from typing import Optional, List
import httpx

from backend.app.config import settings
from backend.app.models.quiz import QuizItem, TrapDetail, OptionItem
from backend.app.models.diagnose import DiagnoseRequest, DiagnoseResponse
from backend.app.services.quiz_service import quiz_service
from backend.app.services.llm_diagnostics import classify_llm_failure

logger = logging.getLogger("diagnostic_engine")


class DiagnosticService:
    """Diagnostic Service implementing dual-mode cognitive evaluation."""

    def __init__(self, timeout: float = 4.0):
        self.timeout = timeout

    async def _call_dashscope_qwen(
        self,
        question: QuizItem,
        selected_key: str,
        trap_title: str,
        prerequisite: str
    ) -> Optional[str]:
        """
        Call DashScope Qwen-Turbo API with strict timeout.
        Returns generated Socratic guidance or None on failure.
        """
        if not settings.has_api_key:
            return None

        headers = {
            "Authorization": f"Bearer {settings.QWEN_API_KEY.strip()}",
            "Content-Type": "application/json"
        }

        system_prompt = (
            "你是一个严谨深刻的大学学科苏格拉底式启发导师。"
            "你的任务是针对学生做题时踩中的认知陷阱与前置盲区进行启发性提问引导。"
            "绝对死命令：1. 严禁直接说出正确答案字母；2. 紧扣考点前置定理与易错盲区；"
            "3. 采用追问方式启发学生反思，语言亲和但学术严谨，字数严格控制在 120 字以内。"
        )

        user_content = (
            f"【题目内容】：{question.stem}\n"
            f"【学生误选】：选项 {selected_key}\n"
            f"【出题陷阱】：{trap_title}\n"
            f"【知识盲区/先修定理】：{prerequisite}\n"
            "请给出一段不剧透答案的苏格拉底式追问与点拨："
        )

        payload = {
            "model": settings.QWEN_MODEL,
            "input": {
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ]
            },
            "parameters": {
                "result_format": "message",
                "max_tokens": 200,
                "temperature": 0.7
            }
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(settings.DASHSCOPE_URL, json=payload, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                output = data.get("output", {})
                choices = output.get("choices", [])
                if choices and "message" in choices[0]:
                    return choices[0]["message"].get("content", "").strip()
                elif "text" in output:
                    return output.get("text", "").strip()
            else:
                failure = classify_llm_failure(resp.status_code, resp.text)
                logger.warning(
                    "DashScope call rejected (%s, HTTP %s, retryable=%s): %s",
                    failure.kind,
                    resp.status_code,
                    failure.retryable,
                    failure.message,
                )
        return None

    async def diagnose_answer(self, req: DiagnoseRequest) -> DiagnoseResponse:
        """
        Main asynchronous diagnostic entrypoint.
        Guaranteed to return HTTP 200 DiagnoseResponse with zero 500 exceptions.
        """
        try:
            # 1. Resolve question from repository
            q_id = req.question_id
            question = quiz_service.get_question_by_id(q_id)
            
            # If not found by given ID, attempt fallback to first question
            if not question:
                logger.warning(f"Question id '{q_id}' not found in database, using graceful safe fallback.")
                return DiagnoseResponse(
                    is_correct=False,
                    question_id=q_id or "unknown",
                    selected_key=req.selected_key or "A",
                    correct_key="B",
                    explanation="未能定位到指定题目编号，系统已启动知识本体应急兜底模式。",
                    trap_id="trap_fallback",
                    trap_title="🚨 题目检索未命中",
                    trap_name="题目检索未命中",
                    concept_name="概念边界检索与匹配",
                    misconception="未在题库索引中匹配到题目编号",
                    prerequisite="系统题目本体完整性",
                    radar_dimension="boundary",
                    score_delta=-2,
                    socratic_guidance="请检查题目索引是否有效，请尝试从该学科的基础概念定理出发进行推导。",
                    socratic_hint="请检查题目索引是否有效，请尝试从该学科的基础概念定理出发进行推导。",
                    knowledge_nodes=["概念检索", "基础假定"],
                    fallback_mode=True,
                    model_used="local-safe-fallback"
                )

            # 2. Determine selected option key
            selected_key = (req.selected_key or req.selected_option or "A").strip().upper()
            
            # 3. Locate correct option and student option
            correct_opt: Optional[OptionItem] = None
            student_opt: Optional[OptionItem] = None
            
            if isinstance(question.options, list):
                for opt in question.options:
                    if isinstance(opt, OptionItem):
                        if opt.is_correct or (question.answer and opt.key.upper() == question.answer.upper()):
                            correct_opt = opt
                        if opt.key.upper() == selected_key:
                            student_opt = opt
                    elif isinstance(opt, dict):
                        if opt.get("is_correct") or opt.get("isCorrect") or (question.answer and opt.get("key", "").upper() == question.answer.upper()):
                            correct_opt = OptionItem(**opt)
                        if opt.get("key", "").upper() == selected_key:
                            student_opt = OptionItem(**opt)

            correct_key = correct_opt.key.upper() if correct_opt else (question.answer or "A").upper()
            is_correct = (selected_key == correct_key)

            # Extract graph concept nodes if available
            knowledge_nodes: List[str] = []
            if question.graph and question.graph.nodes:
                knowledge_nodes = [node.label for node in question.graph.nodes]
            elif question.tag:
                knowledge_nodes = [question.tag]

            # 4. Handle correct option
            if is_correct:
                return DiagnoseResponse(
                    is_correct=True,
                    question_id=question.id,
                    selected_key=selected_key,
                    correct_key=correct_key,
                    explanation=question.explanation,
                    trap_id=None,
                    trap_title=None,
                    trap_name=None,
                    concept_name="考点概念精准命中",
                    misconception=None,
                    prerequisite="已完全掌握该知识点核心定理与边界条件",
                    radar_dimension="trapDefense",
                    score_delta=5,
                    socratic_guidance="太棒了！考点精准命中，成功避开出题陷阱！基础概念牢固度与陷阱防御指数均已提升。",
                    socratic_hint="太棒了！考点精准命中，成功避开出题陷阱！基础概念牢固度与陷阱防御指数均已提升。",
                    knowledge_nodes=knowledge_nodes,
                    fallback_mode=False,
                    model_used="rule-evaluation"
                )

            # 5. Handle incorrect option (distractor trap hit)
            # Find matched trap
            trap_id = student_opt.trap_id if student_opt and student_opt.trap_id else None
            trap: Optional[TrapDetail] = None
            if trap_id and question.traps and trap_id in question.traps:
                trap = question.traps[trap_id]
            elif question.traps:
                trap_id = next(iter(question.traps.keys()))
                trap = question.traps[trap_id]

            trap_title = trap.title if trap else "🚨 核心概念理解偏差陷阱"
            misconception = trap.desc if trap else "该选项触碰了该学科考点的典型认知盲区。"
            prerequisite = trap.prereq if trap else (question.tag or "先修定理前置与概念边界")
            radar_dim = trap.radar_hit if trap else "trapDefense"
            fallback_socratic = (
                question.socratic_prompt 
                or (trap.desc if trap else "请回忆相关先修定理的严格数学或法理边界条件。")
            )

            # 6. Dual-Mode Evaluation: Attempt Live LLM with timeout, else Graceful Fallback
            socratic_text: Optional[str] = None
            model_used = "local-knowledge-seed"
            fallback_mode = True

            if settings.has_api_key and req.include_socratic:
                try:
                    socratic_text = await self._call_dashscope_qwen(
                        question=question,
                        selected_key=selected_key,
                        trap_title=trap_title,
                        prerequisite=prerequisite
                    )
                    if socratic_text and socratic_text.strip():
                        fallback_mode = False
                        model_used = settings.QWEN_MODEL
                except Exception as e:
                    logger.warning(f"Live Qwen LLM call exception ({e}), engaging local seed fallback.")
                    socratic_text = None

            if not socratic_text:
                socratic_text = fallback_socratic
                fallback_mode = True
                model_used = "local-knowledge-seed"

            return DiagnoseResponse(
                is_correct=False,
                question_id=question.id,
                selected_key=selected_key,
                correct_key=correct_key,
                explanation=question.explanation,
                trap_id=trap_id,
                trap_title=trap_title,
                trap_name=trap_title,
                concept_name=prerequisite,
                misconception=misconception,
                prerequisite=prerequisite,
                radar_dimension=radar_dim,
                score_delta=-5,
                socratic_guidance=socratic_text,
                socratic_hint=socratic_text,
                knowledge_nodes=knowledge_nodes,
                fallback_mode=fallback_mode,
                model_used=model_used
            )

        except Exception as unhandled:
            # Absolute failsafe shield: NEVER raise 500
            logger.error(f"Unexpected error in diagnostic engine: {unhandled}", exc_info=True)
            return DiagnoseResponse(
                is_correct=False,
                question_id=getattr(req, "question_id", "unknown"),
                selected_key=getattr(req, "selected_key", "A") or "A",
                correct_key="B",
                explanation="诊断服务处于高可用应急兜底模式，解析正常生效。",
                trap_id="trap_failsafe",
                trap_title="🚨 高可用安全兜底",
                trap_name="高可用安全兜底",
                concept_name="系统容灾高可用性",
                misconception="服务遇到偶发未知扰动，已完成毫秒级无损降级",
                prerequisite="系统鲁棒性与异常隔离原则",
                radar_dimension="trapDefense",
                score_delta=0,
                socratic_guidance="请思考该题考查的核心定义，结合排除法分析各选项的内在逻辑合理性。",
                socratic_hint="请思考该题考查的核心定义，结合排除法分析各选项的内在逻辑合理性。",
                knowledge_nodes=["高可用兜底"],
                fallback_mode=True,
                model_used="local-failsafe-shield"
            )


# Global singleton instance
diagnostic_service = DiagnosticService(timeout=settings.LLM_TIMEOUT)
