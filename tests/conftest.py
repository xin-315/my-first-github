"""
Pytest configuration and shared fixtures for JC2001 Smart Study Assistant System.
"""

import os
import sys
import warnings
from pathlib import Path
from typing import Generator
import pytest

# Filter deprecation warnings from Starlette/httpx test client
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Ensure project root is at the front of sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from starlette.testclient import TestClient


@pytest.fixture(autouse=True)
def clean_test_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Ensure each test runs with a deterministic testing environment.
    By default, clear live LLM API keys so resilient offline fallback is exercised
    unless a specific test explicitly injects a mock or real key.
    """
    monkeypatch.setenv("TESTING", "true")
    monkeypatch.delenv("DASHSCOPE_API_KEY", raising=False)
    monkeypatch.delenv("QWEN_API_KEY", raising=False)


@pytest.fixture(scope="session")
def app():
    """
    Load the FastAPI application instance.
    Supports either backend.app.main:app or backend.main:app.
    """
    try:
        from backend.app.main import app as fastapi_app
        return fastapi_app
    except ImportError:
        from backend.main import app as fastapi_app
        return fastapi_app


@pytest.fixture(scope="session")
def client(app) -> Generator[TestClient, None, None]:
    """
    Provide an in-memory Starlette/FastAPI TestClient for high-speed opaque-box API tests.
    """
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client


@pytest.fixture
def econ_distractor_payload() -> dict:
    """Sample wrong distractor option for Econometrics (OLS biased trap)."""
    return {
        "question_id": "econ_1",
        "selected_option": "A"
    }


@pytest.fixture
def econ_correct_payload() -> dict:
    """Sample correct option for Econometrics (C: OLS依然保持无偏性与BLUE性质)."""
    return {
        "question_id": "econ_1",
        "selected_option": "C"
    }


@pytest.fixture
def law_distractor_payload() -> dict:
    """Sample wrong distractor option for Law (除斥期间 vs 诉讼时效)."""
    return {
        "question_id": "law_1",
        "selected_option": "A"
    }


@pytest.fixture
def cs_distractor_payload() -> dict:
    """Sample wrong distractor option for Computer Science."""
    return {
        "question_id": "cs_1",
        "selected_option": "A"
    }


@pytest.fixture
def se_distractor_payload() -> dict:
    """Sample wrong distractor option for Software Engineering (A: 强制推行纯瀑布模型)."""
    return {
        "question_id": "se_1",
        "selected_option": "A"
    }
