"""
Diagnostic Engine Request and Response Models
Dual-mode schema with full camelCase / snake_case interoperability and dual serialization.
"""

from typing import List, Optional, Any
from pydantic import Field, model_validator
from backend.app.models.common import CamelModel


class DiagnoseRequest(CamelModel):
    """Payload for POST /api/diagnose."""
    question_id: str = Field(default="", description="Target question ID (e.g. econ_1)")
    questionId: Optional[str] = Field(default="", description="CamelCase alias for question_id")
    selected_key: Optional[str] = Field(default=None, description="Chosen option key: A, B, C, or D")
    selectedKey: Optional[str] = Field(default=None, description="CamelCase alias for selected_key")
    selected_option: Optional[str] = Field(default=None, description="Alias for selected_key")
    selectedOption: Optional[str] = Field(default=None, description="CamelCase alias for selected_option")
    subject: Optional[str] = Field(default=None, description="Discipline code (optional)")
    user_answer_text: Optional[str] = Field(default=None, description="Optional selected text")
    userAnswerText: Optional[str] = Field(default=None, description="CamelCase alias for user_answer_text")
    include_socratic: bool = Field(default=True, description="Whether to generate Socratic guidance")
    includeSocratic: Optional[bool] = Field(default=True, description="CamelCase alias for include_socratic")

    @model_validator(mode="before")
    @classmethod
    def normalize_keys(cls, data: Any) -> Any:
        if isinstance(data, dict):
            # Resolve question_id from multiple alias candidates
            q_id = data.get("question_id") or data.get("questionId") or data.get("id") or ""
            data["question_id"] = q_id
            data["questionId"] = q_id
            
            # Resolve selected key/option
            key = (
                data.get("selected_key") 
                or data.get("selectedKey") 
                or data.get("selected_option") 
                or data.get("selectedOption")
                or data.get("option")
            )
            data["selected_key"] = key
            data["selectedKey"] = key
            data["selected_option"] = key
            data["selectedOption"] = key
            
            # Text & Socratic
            txt = data.get("user_answer_text") or data.get("userAnswerText")
            data["user_answer_text"] = txt
            data["userAnswerText"] = txt
            
            soc = data.get("include_socratic") if "include_socratic" in data else data.get("includeSocratic", True)
            data["include_socratic"] = soc
            data["includeSocratic"] = soc
        return data

    @model_validator(mode="after")
    def sync_request(self) -> "DiagnoseRequest":
        choice = self.selected_key or self.selected_option or self.selectedKey or self.selectedOption or ""
        self.selected_key = choice
        self.selectedKey = choice
        self.selected_option = choice
        self.selectedOption = choice
        
        q = self.question_id or self.questionId or ""
        self.question_id = q
        self.questionId = q
        
        soc = bool(self.include_socratic if self.include_socratic is not None else self.includeSocratic)
        self.include_socratic = soc
        self.includeSocratic = soc
        return self


class DiagnoseResponse(CamelModel):
    """
    Response returned by POST /api/diagnose.
    Fully compatible with PROJECT.md and frontend app.js schemas.
    Serializes both snake_case and camelCase attributes for zero-keyerror guarantees.
    """
    is_correct: bool = Field(default=True, description="Whether the option is correct")
    isCorrect: bool = Field(default=True, description="CamelCase alias for is_correct")
    question_id: str = Field(default="", description="Target question ID")
    questionId: str = Field(default="", description="CamelCase alias for question_id")
    selected_key: str = Field(default="", description="Selected option letter")
    selectedKey: str = Field(default="", description="CamelCase alias for selected_key")
    correct_key: str = Field(default="", description="True answer option letter")
    correctKey: str = Field(default="", description="CamelCase alias for correct_key")
    explanation: str = Field(default="", description="Authoritative question explanation")
    
    # Trap and Misconception attributes
    trap_id: Optional[str] = Field(default=None, description="Matched distractor trap ID")
    trapId: Optional[str] = Field(default=None, description="CamelCase alias for trap_id")
    trap_title: Optional[str] = Field(default=None, description="Misconception heading")
    trapTitle: Optional[str] = Field(default=None, description="CamelCase alias for trap_title")
    trap_name: Optional[str] = Field(default=None, description="Alias for trap_title (PROJECT.md)")
    trapName: Optional[str] = Field(default=None, description="CamelCase alias for trap_name")
    
    concept_name: Optional[str] = Field(default=None, description="Missed core prerequisite concept (PROJECT.md)")
    conceptName: Optional[str] = Field(default=None, description="CamelCase alias for concept_name")
    misconception: Optional[str] = Field(default=None, description="In-depth misconception reasoning")
    prerequisite: Optional[str] = Field(default=None, description="Foundational theorem or boundary missed")
    radar_dimension: Optional[str] = Field(default=None, description="Penalized radar dimension")
    radarDimension: Optional[str] = Field(default=None, description="CamelCase alias for radar_dimension")
    score_delta: int = Field(default=0, description="Mastery delta (+5 or -5)")
    scoreDelta: int = Field(default=0, description="CamelCase alias for score_delta")
    
    # Socratic guidance attributes
    socratic_guidance: Optional[str] = Field(default=None, description="Socratic dialogue guidance (PROJECT.md)")
    socraticGuidance: Optional[str] = Field(default=None, description="CamelCase alias for socratic_guidance")
    socratic_hint: Optional[str] = Field(default=None, description="Alias for socratic_guidance")
    socraticHint: Optional[str] = Field(default=None, description="CamelCase alias for socratic_hint")
    knowledge_nodes: List[str] = Field(default_factory=list, description="Graph concept nodes")
    knowledgeNodes: List[str] = Field(default_factory=list, description="CamelCase alias for knowledge_nodes")
    
    # Fault-tolerance and execution mode
    fallback_mode: bool = Field(default=False, description="True if served by offline seed fallback")
    fallbackMode: bool = Field(default=False, description="CamelCase alias for fallback_mode")
    model_used: Optional[str] = Field(default="local-knowledge-seed", description="Inference engine identifier")
    modelUsed: Optional[str] = Field(default="local-knowledge-seed", description="CamelCase alias for model_used")

    @model_validator(mode="before")
    @classmethod
    def normalize_input(cls, data: Any) -> Any:
        if isinstance(data, dict):
            # Normalize is_correct
            c = data.get("is_correct") if "is_correct" in data else data.get("isCorrect", True)
            data["is_correct"] = bool(c)
            data["isCorrect"] = bool(c)
            
            # Normalize IDs & keys
            q = data.get("question_id") or data.get("questionId") or ""
            data["question_id"] = q
            data["questionId"] = q
            
            sk = data.get("selected_key") or data.get("selectedKey") or ""
            data["selected_key"] = sk
            data["selectedKey"] = sk
            
            ck = data.get("correct_key") or data.get("correctKey") or ""
            data["correct_key"] = ck
            data["correctKey"] = ck
            
            # Trap
            tid = data.get("trap_id") or data.get("trapId")
            data["trap_id"] = tid
            data["trapId"] = tid
            
            tt = data.get("trap_title") or data.get("trapTitle") or data.get("trap_name") or data.get("trapName")
            data["trap_title"] = tt
            data["trapTitle"] = tt
            data["trap_name"] = tt
            data["trapName"] = tt
            
            cn = data.get("concept_name") or data.get("conceptName") or data.get("prerequisite")
            data["concept_name"] = cn
            data["conceptName"] = cn
            data["prerequisite"] = data.get("prerequisite") or cn
            
            # Radar & score
            rd = data.get("radar_dimension") or data.get("radarDimension")
            data["radar_dimension"] = rd
            data["radarDimension"] = rd
            
            sd = data.get("score_delta") if "score_delta" in data else data.get("scoreDelta", 0)
            data["score_delta"] = sd
            data["scoreDelta"] = sd
            
            # Socratic
            sg = data.get("socratic_guidance") or data.get("socraticGuidance") or data.get("socratic_hint") or data.get("socraticHint")
            data["socratic_guidance"] = sg
            data["socraticGuidance"] = sg
            data["socratic_hint"] = sg
            data["socraticHint"] = sg
            
            # Nodes
            kn = data.get("knowledge_nodes") if "knowledge_nodes" in data else data.get("knowledgeNodes", [])
            data["knowledge_nodes"] = kn
            data["knowledgeNodes"] = kn
            
            # Fallback & model
            fb = data.get("fallback_mode") if "fallback_mode" in data else data.get("fallbackMode", False)
            data["fallback_mode"] = bool(fb)
            data["fallbackMode"] = bool(fb)
            
            mu = data.get("model_used") or data.get("modelUsed") or "local-knowledge-seed"
            data["model_used"] = mu
            data["modelUsed"] = mu
        return data

    @model_validator(mode="after")
    def sync_all_interop_fields(self) -> "DiagnoseResponse":
        # Core flags
        c = bool(self.is_correct or self.isCorrect)
        self.is_correct = c
        self.isCorrect = c
        
        q = self.question_id or self.questionId or ""
        self.question_id = q
        self.questionId = q
        
        sk = self.selected_key or self.selectedKey or ""
        self.selected_key = sk
        self.selectedKey = sk
        
        ck = self.correct_key or self.correctKey or ""
        self.correct_key = ck
        self.correctKey = ck
        
        # Traps & Concepts
        tid = self.trap_id or self.trapId
        self.trap_id = tid
        self.trapId = tid
        
        effective_title = self.trap_title or self.trap_name or self.trapTitle or self.trapName
        self.trap_title = effective_title
        self.trap_name = effective_title
        self.trapTitle = effective_title
        self.trapName = effective_title
        
        effective_concept = self.prerequisite or self.concept_name or self.conceptName
        self.concept_name = effective_concept
        self.prerequisite = effective_concept
        self.conceptName = effective_concept
        
        rd = self.radar_dimension or self.radarDimension
        self.radar_dimension = rd
        self.radarDimension = rd
        
        sd = self.score_delta if self.score_delta != 0 else self.scoreDelta
        self.score_delta = sd
        self.scoreDelta = sd
        
        # Socratic text
        s_text = self.socratic_guidance or self.socratic_hint or self.socraticGuidance or self.socraticHint
        self.socratic_guidance = s_text
        self.socratic_hint = s_text
        self.socraticGuidance = s_text
        self.socraticHint = s_text
        
        # Knowledge and mode
        kn = self.knowledge_nodes if self.knowledge_nodes else self.knowledgeNodes
        self.knowledge_nodes = kn
        self.knowledgeNodes = kn
        
        fb = bool(self.fallback_mode or self.fallbackMode)
        self.fallback_mode = fb
        self.fallbackMode = fb
        
        mu = self.model_used or self.modelUsed or "local-knowledge-seed"
        self.model_used = mu
        self.modelUsed = mu
        
        return self
