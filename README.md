# JC2001 Group 5: Smart Study Assistant System (智学罗盘)

An intelligent study and misconception-diagnostic assistant powered by Knowledge Graphs and LLMs, developed for undergraduate STEM and professional exam preparation.

Course: **JC2001 Introduction to Software Engineering (Academic Year 2026–27)**  
Institution: **University of Aberdeen**  
Degree Programme: **BSc in Business Management and Information Systems (BSc BMIS)**  
Academic Supervisor: **Dr. Shahzad Mumtaz** (`shahzad.mumtaz@abdn.ac.uk`)  

---

## 👥 Team Roster (Group 5)

| # | Name | Student ID | Primary Role | Area of Responsibility |
| :-: | :--- | :-: | :--- | :--- |
| 1 | **吴宇轩 (Yuxuan Wu)** | `50106070` | **Team Leader & Project Manager** | Overall governance, sprint tracking & course liaison |
| 2 | **林泳桐 (Yongtong Lin)** | `50106038` | **Lead Business Analyst** | Requirements elicitation, use case modeling & concept originator |
| 3 | **王思鉴 (Sijian Wang)** | `50106045` | **System Architect** | UML architecture, context models & Neo4j graph ontology |
| 4 | **江昊 (Hao Jiang)** | `50106065` | **PoC Lead Developer** | Backend API scaffolding, Neo4j driver & GraphRAG engine |
| 5 | **谢炜昕 (Weixin Xie)** | `50106034` | **QA & Technical Report Lead** | Report master coordination, citation integrity & concept originator |
| 6 | **张梓健 (Zijian Zhang)** | `50106035` | **Business Analyst** | User stories, non-functional requirements & acceptance criteria |
| 7 | **习羽赛 (Yusai Xi)** | `50105989` | **UI/UX Designer** | Wireframes, console interface layout & interaction flow |
| 8 | **董思钦 (Siqin Dong)** | `50106060` | **PoC Logic Developer** | Diagnostic prompt engineering & quiz logic services |
| 9 | **杨明杰 (Mingjie Yang)** | `50106061` | **Software Testing Lead** | Test plan formulation, black-box test cases & user manual |
| 10 | **梁子铉 (Zixuan Liang)** | `50106037` | **Deployment & Media Lead** | Environment setup, Git workflow discipline & video presentation |

---

## 📂 Repository Structure

```text
d:/jc2001/
├── frontend/             # DeepSeek Console-styled Web Frontend (HTML, CSS, JS)
│   ├── index.html        # Main dashboard SPA
│   ├── style.css         # Console styling (light/dark theme)
│   └── app.js            # Client-side interaction logic
├── graphrag（终）/        # PoC prototypes & exploratory benchmark evaluation
│   ├── real_graph_engine.py  # Streamlit prototype with Neo4j & Qwen
│   ├── systematic_eval_engine.py # Multi-discipline benchmark evaluation
│   └── *.csv             # Evaluation datasets (law, CS, statistics, etc.)
├── reports/              # Official Coursework Deliverables & Technical Reports
│   ├── project_proposal.pdf  # Formal Project Proposal (Submitted Sep 25)
│   ├── project_proposal.md   # Proposal markdown master
│   ├── week1_team_review_pack.pdf # Team review document
│   ├── week2_execution_guide.md   # Phase 2 Week 2 Team Execution Plan
│   └── competitor_analysis.md     # Competitive & cognitive architecture analysis
├── scripts/              # Automated verification & document generation utilities
│   ├── verify_week1_deliverables.py # Quality gate validation script
│   └── generate_proposal_docs.py    # Automated docx/pdf compiler
├── practical1_deliverables.md # Complete icebreaker & role allocation records
├── .gitignore            # Git exclusion rules
└── README.md             # This document
```

---

## 🚀 Quickstart for Team Members

### 1. Environment Setup
- Python 3.10+ recommended.
- Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Running Local Frontend
Open `frontend/index.html` directly in any modern browser (Chrome, Edge, Firefox).

### 3. Running Verification Suite
Verify deliverable consistency and quality gates:
```bash
python scripts/verify_week1_deliverables.py
```

---

## 📜 Development & Git Guidelines
- All major features should be developed in dedicated feature branches (e.g., `feat-requirements`, `feat-api`).
- Never commit credentials (`.env`, API tokens) or temporary caches.
- Please refer to [Phase 2 Execution Guide](file:///d:/jc2001/reports/week2_execution_guide.md) for detailed weekly responsibilities.
