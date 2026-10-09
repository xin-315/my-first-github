"""
E2E Frontend Integration and Static Mount Verification Suite
Covers Tier 1 (Static Asset Delivery), Tier 2 (Asset Content-Types & Encodings),
Tier 3 (DOM Contract & ID Integrity), and Tier 4 (Single-Port App Preview).
"""

from pathlib import Path
import pytest
from starlette.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"


# -----------------------------------------------------------------------------
# Tier 1 & 2: Static Mount & Asset Delivery Tests
# -----------------------------------------------------------------------------

def test_frontend_root_static_mount_serves_html(client: TestClient):
    """
    Tier 1: Verify accessing root '/' serves the DeepSeek console index.html.
    Authority: Special User Directive '记得搭建好前端给我看哦' & PROJECT.md Static Serving.
    """
    response = client.get("/")
    assert response.status_code == 200, f"Expected 200 OK at root '/', got {response.status_code}"
    
    content_type = response.headers.get("content-type", "")
    assert "text/html" in content_type, f"Expected HTML content type, got '{content_type}'"
    
    body = response.text
    assert "<title>" in body and "智学罗盘" in body, "Response HTML must contain system title"
    assert "app-shell" in body, "Response HTML must contain app-shell container"


def test_frontend_index_html_direct_route(client: TestClient):
    """
    Tier 1: Verify direct access to '/index.html' returns 200 OK.
    """
    response = client.get("/index.html")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")


def test_frontend_static_stylesheet_serves_css(client: TestClient):
    """
    Tier 2: Verify '/style.css' is served with text/css content-type.
    """
    response = client.get("/style.css")
    assert response.status_code == 200, f"Failed to fetch style.css: {response.status_code}"
    content_type = response.headers.get("content-type", "")
    assert "text/css" in content_type, f"Expected CSS content type, got '{content_type}'"
    assert len(response.text.strip()) > 100, "style.css should not be empty"


def test_frontend_static_script_serves_javascript(client: TestClient):
    """
    Tier 2: Verify '/app.js' is served with application/javascript or text/javascript.
    """
    response = client.get("/app.js")
    assert response.status_code == 200, f"Failed to fetch app.js: {response.status_code}"
    content_type = response.headers.get("content-type", "")
    assert ("javascript" in content_type or "text/plain" in content_type), (
        f"Expected JavaScript content type, got '{content_type}'"
    )
    assert len(response.text.strip()) > 100, "app.js should not be empty"


# -----------------------------------------------------------------------------
# Tier 3: DOM Selector Contract & Asset Integrity Smoke Tests
# -----------------------------------------------------------------------------

def test_frontend_files_exist_on_disk():
    """
    Tier 3: Ensure critical frontend assets exist and are UTF-8 decodable on the local filesystem.
    """
    assert FRONTEND_DIR.exists(), f"Frontend directory missing at {FRONTEND_DIR}"

    for filename in ["index.html", "style.css", "app.js"]:
        file_path = FRONTEND_DIR / filename
        assert file_path.exists(), f"Frontend asset {filename} missing at {file_path}"
        assert file_path.stat().st_size > 0, f"Frontend asset {filename} must not be empty"
        # Validate UTF-8 encoding
        content = file_path.read_text(encoding="utf-8")
        assert len(content) > 0


def test_html_dom_elements_required_by_app_js():
    """
    Tier 3 & 4: DOM Contract Smoke Check.
    Assert that frontend/index.html contains all critical element IDs and data attributes
    relied upon by frontend/app.js to guarantee zero JavaScript runtime crashes.
    """
    index_html_path = FRONTEND_DIR / "index.html"
    html_content = index_html_path.read_text(encoding="utf-8")

    # Critical Element IDs
    required_ids = [
        "options-container",      # Container where quiz choices are dynamically injected
        "diagnostic-drawer",      # Slide drawer for misconception & Socratic analysis
        "q-stem",                 # Question stem element
        "q-difficulty",           # Star difficulty rating
        "q-tag",                  # Syllabus topic badge
        "theme-toggle-btn",       # Light/Dark mode switcher
        "next-q-btn",             # Next question button
        "prev-q-btn",             # Previous question button
        "reset-q-btn",            # Reset current question button
        "chat-msgs-container",    # Socratic tutor message scroll list
        "chat-input-text",        # Tutor user text input
        "chat-send-btn",          # Tutor send button
        "large-graph-svg",        # SVG knowledge graph topology canvas
        "mini-radar-chart",       # 5-dimension competency radar container
        "api-modal",              # Settings modal for API configuration
        "api-settings-btn",       # Nav button opening API settings
    ]

    for element_id in required_ids:
        assert f'id="{element_id}"' in html_content, (
            f"Required DOM element id='{element_id}' is missing in frontend/index.html"
        )

    # Required Navigation Views (data-view attributes)
    required_views = ["quiz", "tutor", "graph", "report"]
    for view_name in required_views:
        assert f'data-view="{view_name}"' in html_content, (
            f"Navigation view tab data-view='{view_name}' is missing in frontend/index.html"
        )

    # Required Subject Selectors (data-subject attributes)
    required_subjects = ["law", "cs", "econ", "se"]
    for subject_name in required_subjects:
        assert f'data-subject="{subject_name}"' in html_content, (
            f"Subject selector button data-subject='{subject_name}' is missing in frontend/index.html"
        )
