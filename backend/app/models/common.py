"""
Common Base Models and Schemas
"""

from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, model_validator


class CamelModel(BaseModel):
    """
    Base Pydantic model with bidirectional camelCase / snake_case interoperability.
    Supports attribute access and dict serialization with population by field name or alias.
    """
    model_config = ConfigDict(
        populate_by_name=True,
        extra="allow"
    )


class HealthResponse(CamelModel):
    """Response payload for GET /api/health."""
    status: str = Field("ok", description="Health status string")
    service: str = Field("smartstudy-poc", description="Service identifier")
    version: str = Field("1.0.0", description="API semantic version")
    mode: str = Field("dual-mode", description="Diagnostic engine operation mode")
    has_api_key: bool = Field(False, description="Whether live LLM API key is detected")
    hasApiKey: Optional[bool] = Field(False, description="CamelCase alias for has_api_key")

    @model_validator(mode="before")
    @classmethod
    def normalize_input(cls, data):
        if isinstance(data, dict):
            val = data.get("has_api_key") if "has_api_key" in data else data.get("hasApiKey", False)
            data["has_api_key"] = val
            data["hasApiKey"] = val
        return data

    @model_validator(mode="after")
    def sync_aliases(self) -> "HealthResponse":
        self.hasApiKey = self.has_api_key
        return self


class LlmHealthResponse(CamelModel):
    """
    Response payload for GET /api/health/llm.

    Reports the outcome of one real probe against the configured Qwen endpoint, so an
    unusable key is visible as data instead of only as a silently degraded diagnosis.
    """
    ok: bool = Field(False, description="Whether the live LLM call path is usable right now")
    kind: str = Field("unknown", description="no_key / auth / rate_limit / timeout / network / server / payload / ok")
    message: str = Field("", description="Human-readable outcome of the probe")
    model: str = Field("", description="Model that was probed")
    endpoint: str = Field("", description="DashScope endpoint that was probed")
    api_key_masked: str = Field("", description="Masked API key (the full key is never returned)")
    apiKeyMasked: Optional[str] = Field("", description="CamelCase alias for api_key_masked")
    latency_ms: Optional[float] = Field(None, description="Round-trip time of the probe in milliseconds")
    latencyMs: Optional[float] = Field(None, description="CamelCase alias for latency_ms")
    status_code: Optional[int] = Field(None, description="HTTP status returned by DashScope, when there was one")
    statusCode: Optional[int] = Field(None, description="CamelCase alias for status_code")
    retryable: bool = Field(False, description="Whether retrying the same call could succeed")
    suggestion: Optional[str] = Field(None, description="Actionable next step for the operator")
    details: dict = Field(default_factory=dict, description="Extra diagnostic context (kept small)")

    @model_validator(mode="after")
    def sync_aliases(self) -> "LlmHealthResponse":
        self.apiKeyMasked = self.api_key_masked
        self.latencyMs = self.latency_ms
        self.statusCode = self.status_code
        return self
