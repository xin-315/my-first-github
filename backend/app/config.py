"""
JC2001 Smart Study Assistant - Application Configuration
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env if present
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

class Settings:
    """Application runtime configuration settings."""
    PROJECT_NAME: str = "JC2001 Smart Study Assistant System PoC MVP"
    SERVICE_ID: str = "smartstudy-poc"
    VERSION: str = "1.0.0"
    
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # DashScope / Qwen credentials with multi-variable fallback
    QWEN_API_KEY: str = os.getenv("QWEN_API_KEY") or os.getenv("DASHSCOPE_API_KEY") or ""
    DASHSCOPE_URL: str = os.getenv(
        "DASHSCOPE_URL", 
        "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    )
    QWEN_MODEL: str = os.getenv("QWEN_MODEL", "qwen-turbo")
    LLM_TIMEOUT: float = float(os.getenv("LLM_TIMEOUT", "4.0"))
    
    # Frontend directory path
    FRONTEND_DIR: Path = BASE_DIR / "frontend"

    @property
    def has_api_key(self) -> bool:
        return bool(self.QWEN_API_KEY and self.QWEN_API_KEY.strip())


settings = Settings()
