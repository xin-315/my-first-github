"""
Quiz Domain Schemas and Models
Pydantic v2 compatible schemas with bidirectional camelCase / snake_case support.
"""

from typing import List, Dict, Optional, Any, Union
from pydantic import Field, model_validator
from backend.app.models.common import CamelModel


class OptionItem(CamelModel):
    """Single multiple-choice option with dual case support."""
    key: str = Field(..., description="Option letter: A, B, C, D")
    text: str = Field(..., description="Option description text")
    is_correct: bool = Field(default=False, description="Whether this is the correct answer")
    isCorrect: Optional[bool] = Field(default=False, description="CamelCase alias for is_correct")
    trap_id: Optional[str] = Field(default=None, description="Associated distractor trap identifier")
    trapId: Optional[str] = Field(default=None, description="CamelCase alias for trap_id")

    @model_validator(mode="before")
    @classmethod
    def normalize_keys(cls, data: Any) -> Any:
        if isinstance(data, dict):
            # Normalize is_correct
            c = data.get("is_correct") if "is_correct" in data else data.get("isCorrect", False)
            data["is_correct"] = bool(c)
            data["isCorrect"] = bool(c)
            # Normalize trap_id
            t = data.get("trap_id") if "trap_id" in data else data.get("trapId")
            data["trap_id"] = t
            data["trapId"] = t
        return data

    @model_validator(mode="after")
    def sync_aliases(self) -> "OptionItem":
        val = bool(self.is_correct or self.isCorrect)
        self.is_correct = val
        self.isCorrect = val
        
        t = self.trap_id or self.trapId
        self.trap_id = t
        self.trapId = t
        return self


class TrapDetail(CamelModel):
    """Detailed trap and misconception metadata with dual case support."""
    title: str = Field(..., description="Trap title and warning tag")
    desc: str = Field(..., description="Detailed misconception description")
    prereq: str = Field(..., description="Prerequisite theorem or conceptual boundary")
    radar_hit: str = Field(default="trapDefense", description="Associated radar dimension")
    radarHit: Optional[str] = Field(default="trapDefense", description="CamelCase alias for radar_hit")

    @model_validator(mode="before")
    @classmethod
    def normalize_keys(cls, data: Any) -> Any:
        if isinstance(data, dict):
            r = data.get("radar_hit") or data.get("radarHit") or "trapDefense"
            data["radar_hit"] = r
            data["radarHit"] = r
        return data

    @model_validator(mode="after")
    def sync_aliases(self) -> "TrapDetail":
        r = self.radar_hit or self.radarHit or "trapDefense"
        self.radar_hit = r
        self.radarHit = r
        return self


class GraphNode(CamelModel):
    """Node in knowledge subgraph topology."""
    id: str = Field(..., description="Unique node id")
    label: str = Field(..., description="Display label for concept or trap")
    type: str = Field("core", description="Node role: 'core', 'prereq', or 'trap'")
    x: Optional[float] = Field(0.0, description="X coordinate for canvas positioning")
    y: Optional[float] = Field(0.0, description="Y coordinate for canvas positioning")


class GraphEdge(CamelModel):
    """Directed edge in knowledge subgraph topology."""
    from_node: str = Field(..., alias="from", description="Source node id")
    to_node: str = Field(..., alias="to", description="Target node id")
    label: str = Field(..., description="Semantic edge label, e.g. '易错于', '保证无偏前提'")


class GraphData(CamelModel):
    """Complete knowledge subgraph for a question."""
    title: str = Field(..., description="Knowledge subgraph title")
    nodes: List[GraphNode] = Field(default_factory=list, description="Topological concept nodes")
    edges: List[GraphEdge] = Field(default_factory=list, description="Topological semantic edges")


class QuizItem(CamelModel):
    """
    Curated question item entity with full dual-case serialization.
    Conforms to both the specification in PROJECT.md and the frontend app.js DB schema.
    """
    id: str = Field(default="", description="Question unique identifier, e.g. econ_1, cs_2")
    question_id: Optional[str] = Field(default="", description="Alias for id")
    questionId: Optional[str] = Field(default="", description="CamelCase alias for id")
    subject: str = Field(..., description="Discipline code: econ, cs, law, se")
    difficulty: str = Field("★★★☆☆", description="Star difficulty rating")
    tag: str = Field("", description="Curriculum or syllabus examination point tag")
    stem: str = Field(..., description="Question stem text")
    options: Union[List[OptionItem], Dict[str, Any]] = Field(..., description="List of options or option dict")
    answer: Optional[str] = Field(default=None, description="Correct option key, e.g. B")
    explanation: str = Field(default="", description="Authoritative question analysis and solution")
    trap_hint: Optional[str] = Field(default=None, description="Short hint about question trap")
    trapHint: Optional[str] = Field(default=None, description="CamelCase alias for trap_hint")
    traps: Dict[str, TrapDetail] = Field(default_factory=dict, description="Pre-compiled misconception mapping")
    graph: Optional[GraphData] = Field(default=None, description="Interactive knowledge subgraph topology")
    socratic_prompt: Optional[str] = Field(default=None, description="Guiding Socratic prompt")
    socraticPrompt: Optional[str] = Field(default=None, description="CamelCase alias for socratic_prompt")

    @model_validator(mode="before")
    @classmethod
    def normalize_options_and_id(cls, data: Any) -> Any:
        if isinstance(data, dict):
            # Normalize question_id <-> id
            q_id = data.get("id") or data.get("question_id") or data.get("questionId") or ""
            data["id"] = q_id
            data["question_id"] = q_id
            data["questionId"] = q_id
            
            # Normalize prompt
            prompt = data.get("socratic_prompt") or data.get("socraticPrompt")
            data["socratic_prompt"] = prompt
            data["socraticPrompt"] = prompt
            
            # Normalize hint
            hint = data.get("trap_hint") or data.get("trapHint")
            data["trap_hint"] = hint
            data["trapHint"] = hint

            # Normalize options if provided as {"A": "text", "B": "text"}
            raw_opts = data.get("options")
            if isinstance(raw_opts, dict):
                converted = []
                ans = data.get("answer", "")
                for k, v in raw_opts.items():
                    converted.append(OptionItem(
                        key=str(k),
                        text=str(v),
                        is_correct=(str(k).upper() == str(ans).upper())
                    ))
                data["options"] = converted
        return data

    @model_validator(mode="after")
    def sync_post_fields(self) -> "QuizItem":
        # Synchronize id / question_id / questionId
        primary_id = self.id or self.question_id or self.questionId or ""
        self.id = primary_id
        self.question_id = primary_id
        self.questionId = primary_id
        
        # Synchronize socratic prompts
        prompt = self.socratic_prompt or self.socraticPrompt
        self.socratic_prompt = prompt
        self.socraticPrompt = prompt

        # Synchronize trap hints
        th = self.trap_hint or self.trapHint
        if not th and self.traps:
            first_trap = next(iter(self.traps.values()))
            th = getattr(first_trap, "title", str(first_trap))
        self.trap_hint = th
        self.trapHint = th

        # Deduce answer key if not explicitly set
        if not self.answer and isinstance(self.options, list):
            for opt in self.options:
                if isinstance(opt, OptionItem) and opt.is_correct:
                    self.answer = opt.key
                    break
                elif isinstance(opt, dict) and (opt.get("is_correct") or opt.get("isCorrect")):
                    self.answer = opt.get("key")
                    break

        return self
