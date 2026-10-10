# StudyGraph — Consolidated Use Case Specifications (UC-01–UC-08)

**Course:** JC2001 / Group 5  
**Project:** StudyGraph — To Design and Implement a Graph-Grounded Diagnostic Study Assistant  
**Combined by:** Lin Yongtong (50106038), Requirements Lead  
**Individual contributions:** Lin Yongtong — UC-01 to UC-04; Zhang Zijian (50106035) — UC-05 to UC-08  
**Baseline:** `docs/PROJECT_PROPOSAL_DRAFT.md` and supplied StudyGraph implementation  
**Status:** Combined author-attributed draft for group review, 9 October 2026  
**Deadline:** 10 October 2026, 22:00 (Asia/Shanghai)

> **Preservation rule.** Part A describes Lin Yongtong's UC-01–UC-04. Part B reproduces the complete personal document provided by Zhang Zijian through GitHub PR #5 (`9413a58`), including its original title, ownership statement, numbered sections, exceptions, acceptance criteria, implementation notes and sources. The personal-document note that UC-01–UC-04 are not included refers only to Zhang's original personal submission, not to this combined file. Neither student's proposed requirements imply that all features are already implemented or tested.

## Combined use-case index

| Use case | Owner | Title / intended behaviour | Evidence boundary |
| --- | --- | --- | --- |
| UC-01 | Lin Yongtong (50106038) | Incorrect-answer misconception diagnosis | Local API and curated JSON |
| UC-02 | Lin Yongtong (50106038) | Domain-based question practice | Local question selection and answer submission |
| UC-03 | Lin Yongtong (50106038) | Evidence and source-status inspection | Current UI, not free-text concept search |
| UC-04 | Lin Yongtong (50106038) | Question-specific knowledge map | JSON/SVG graph, not live Neo4j |
| UC-05 | Zhang Zijian (50106035) | Five-dimensional learning analysis | Peer specification reproduced unchanged |
| UC-06 | Zhang Zijian (50106035) | Wrong-answer history | Peer specification reproduced unchanged |
| UC-07 | Zhang Zijian (50106035) | Adaptive supplementary practice | Peer specification reproduced unchanged; feature not yet implemented |
| UC-08 | Zhang Zijian (50106035) | Socratic tutor follow-up | Peer specification reproduced unchanged |

## Part A — Use cases written by Lin Yongtong (50106038)

**Implementation note:** The current project uses a Python standard-library HTTP server, local curated JSON, and a browser UI. It does not require login, FastAPI, Neo4j, ECharts or cloud credentials for its baseline workflow. UC-03 is modelled as evidence inspection consistent with the supplied app; the original task brief's free-text concept search is not implemented and requires scope confirmation.

### Use Case UC-01 — Intelligent Misconception Diagnosis

- **Use case ID:** UC-01
- **Name:** Submit an incorrect answer and receive a misconception diagnosis.
- **Primary actor:** University student.
- **Trigger:** The student selects an incorrect option on the displayed multiple-choice question.
- **Preconditions:**
  1. The local StudyGraph server is running and `/api/questions` has supplied the selected question.
  2. The curated question has a valid ID, four options, a correct key, and a misconception/prerequisite mapping for every incorrect option.
  3. The current question has not already been submitted in this on-screen attempt.
- **Postconditions:**
  1. The system shows the named misconception, its explanation, and the suggested prerequisite.
  2. The accepted attempt is appended to browser `localStorage` and contributes to the progress indicators.
  3. The full project explanation remains a separate user action.
- **Main Success Scenario:**
  1. The student reads the question and selects an incorrect distractor.
  2. The browser disables answer options and sends `POST /api/answer` with `{"question_id": "...", "selected": "B"}` (the key is illustrative).
  3. The Python service validates the question and option, and evaluates the answer against the server-side answer key.
  4. The service returns `correct: false`, the correct key, explanation, progress dimensions and a structured misconception object.
  5. The browser highlights the selected wrong option and correct option and displays the misconception's `title`, `detail` and `prerequisite` in the feedback area.
  6. The browser records the successful attempt locally and updates the overall performance and dimensional indicators.
  7. The student can open guided tutoring or explicitly request the full project explanation.
- **Extensions and Exception Flows:**
  - **2a.** The local answer service is unreachable or returns an error: show an answer-submission error, unlock options and do **not** record a successful attempt. There is no independent offline answer-grading substitute when the local HTTP server is down.
  - **3a.** Unknown question ID, malformed JSON or invalid option: the service rejects the request with an HTTP 400-level response; the UI follows the failure branch.
  - **4a.** Correct answer: display confirmation rather than a misconception; see UC-02.
  - **6a.** Browser storage is unavailable: persistence is not guaranteed by the current JavaScript; this is a reliability gap to test, not a completed fallback.
- **Special requirements and acceptance criteria (Lin Yongtong):**
  1. **AT-01-01:** `GET /api/questions` never exposes the correct answer, full explanation or hidden misconception mapping before an answer is submitted.
  2. **AT-01-02:** For a wrong valid selection, `POST /api/answer` returns an incorrect result and a named misconception with its prerequisite; the UI displays this feedback.
  3. **AT-01-03:** Each incorrect A–D option has an associated misconception record in the curated question schema.
  4. **AT-01-04:** A network/API validation failure does not create a successful attempt; the student sees an error and can retry.
  5. **AT-01-05:** The full explanatory answer is available through a separate deliberate action, not automatically disclosed before grading.

- **Trace:** Objective 1 / 2 / 4; FR-02, FR-03, FR-08, NFR-03; `server.py`, `frontend/app.js`, `data/curated/questions.json`.

### Use Case UC-02 — Domain-Based Question Practice and Answer Submission

- **Use case ID:** UC-02
- **Name:** Choose a study domain, load a question and submit one answer.
- **Primary actor:** University student.
- **Trigger:** The student selects a domain or navigates to a question and chooses an option.
- **Preconditions:**
  1. StudyGraph has loaded public questions from `GET /api/questions`.
  2. At least one item exists in the chosen domain for the normal success scenario.
- **Postconditions:** The accepted answer is marked correct or incorrect and saved as one attempt; progress totals are recalculated.
- **Main Success Scenario:**
  1. The student opens the Practice view and selects **Computer Science**, **Software Engineering**, or **All** from the domain selector.
  2. The browser filters its already loaded question array locally by the `domain` field and resets the current index.
  3. The interface shows the question ID position, topic, stem, four options, difficulty and content-review state.
  4. The student can navigate through eligible questions using the previous/next buttons.
  5. The student chooses an option; the UI disables the current answer controls.
  6. The browser sends `POST /api/answer` with the question ID and selected option and receives the evaluation response.
  7. The UI highlights the result, stores an attempt, and updates the learning indicators; a wrong answer additionally follows UC-01.
- **Extensions and Exception Flows:**
  - **1a.** The initial `/api/questions` request fails: the application shows a fatal local-data loading message; it does not silently switch to a remote source.
  - **2a.** No questions match the selected domain: the current implementation does not yet provide a dedicated empty-state message; add and test this behaviour if new domains are introduced.
  - **5a.** Repeated clicks before completion are blocked by the on-screen answered flag and disabled controls; choosing **Retry** starts a new attempt and may generate another history entry.
  - **6a.** Validation/network failure: see UC-01, branch 2a/3a; no accepted attempt is recorded.
- **Special requirements and acceptance criteria (Lin Yongtong):**
  1. **AT-02-01:** Computer Science, Software Engineering, and All filters select their correct subsets of the public questions.
  2. **AT-02-02:** The chosen question displays its topic, stem, four options, difficulty, and review status without revealing the answer key before submission.
  3. **AT-02-03:** A valid option results in one accepted on-screen submission and an attempt record; answer controls are locked after selection.
  4. **AT-02-04:** An invalid option or inaccessible answer service produces an error rather than a falsely recorded result.
  5. **AT-02-05:** Previous/next navigation and explicit retry remain distinguishable from answer submission.

- **Trace:** Objective 1 / 4; FR-01, FR-02, FR-08; `frontend/index.html`, `frontend/app.js`, `server.py`.

### Use Case UC-03 — Inspect Supporting Evidence and Provenance

- **Use case ID:** UC-03
- **Name:** Review the evidence, source notes, and review status associated with the displayed item.
- **Primary actor:** University student.
- **Trigger:** The student views a question and chooses to examine its supporting evidence before or after answering.
- **Preconditions:** The question has already been loaded from `/api/questions` and includes `evidence`, `source` and `review_status` fields.
- **Postconditions:** The student can distinguish project-supplied evidence from formally reviewed material; the question itself is unchanged.
- **Main Success Scenario:**
  1. The student opens a question in the Practice view.
  2. The browser renders the question's `review_status` badge and its evidence-item count.
  3. In the accompanying evidence panel, the student reads each evidence label and explanation.
  4. The browser displays the source name and source note from the question record.
  5. The student checks whether the item is marked **Source review pending**, rather than assuming verification.
  6. The student can use this evidence to explain the answer or proceed to UC-04 to inspect the linked concept graph.
- **Extensions and Exception Flows:**
  - **2a.** The question has an unknown review state or incomplete source metadata: mark the content for author review; do not silently label it verified. This is a proposed quality rule, not a currently implemented on-screen warning.
  - **3a.** An evidence list is empty or malformed: fail project data validation and correct the dataset before assessment; the current validator only requires at least two records, not independent fact-checking.
  - **6a.** Free-text search for concepts across the graph is requested: **not supported in the provided application**; the current scope is question-level inspection, not cross-topic retrieval.
- **Special requirements and acceptance criteria (Lin Yongtong):**
  1. **AT-03-01:** The item displays its supporting evidence entries, source name/note, and `review_status` without implying independent verification.
  2. **AT-03-02:** Items labelled `Source review pending` remain visibly pending; no item is described as formally verified without a completed source audit.
  3. **AT-03-03:** Loading evidence or moving to the evidence view does not add an answer attempt.
  4. **AT-03-04:** Missing or malformed evidence metadata is reported for data correction rather than being fabricated by the UI.

- **Trace:** Objective 1 / 2 / 4; FR-05, NFR-03; `frontend/app.js`, `data/curated/questions.json`, `tools/validate_project.py`.

### Use Case UC-04 — Explore the Question-Specific Knowledge Map

- **Use case ID:** UC-04
- **Name:** Explore related concepts, prerequisites and misconception nodes for the current question.
- **Primary actor:** University student.
- **Trigger:** The student selects the Knowledge Map view and clicks or keyboard-activates a graph node.
- **Preconditions:** A current curated question with valid `graph.nodes` and `graph.edges` is loaded.
- **Postconditions:** The selected node's title and description appear in the detail area without modifying the stored graph.
- **Main Success Scenario:**
  1. The student selects the Knowledge Map navigation item.
  2. The browser reads the current question's graph data from its in-memory question record.
  3. The UI draws an SVG containing `concept`, `prerequisite`, and `misconception` nodes with labelled directional edges.
  4. The student selects a node by mouse click or by focusing it and pressing Enter or Space.
  5. The interface displays the selected node's label and description in the graph-detail region.
  6. The student can select further visible nodes, switch the theme or navigate to another question to view its own predefined graph.
- **Extensions and Exception Flows:**
  - **2a.** No question is selected: graph rendering does nothing; a dedicated empty-state explanation is future work.
  - **3a.** An edge refers to a nonexistent node: project validation should reject the curated item (`tools/validate_project.py`).
  - **4a.** The user expects arbitrary Neo4j traversal, graph expansion or drag-to-reposition behaviour: **not available** in this static JSON/SVG implementation.
  - **4b.** A keyboard user cannot perceive a selected node: verify focus and detail changes during accessibility testing; the browser smoke script checks a clickable node, not a full keyboard audit.
- **Special requirements and acceptance criteria (Lin Yongtong):**
  1. **AT-04-01:** The active question displays a graph containing its defined nodes and typed relationships.
  2. **AT-04-02:** Selecting a valid node changes the visible detail panel to show that node's information.
  3. **AT-04-03:** Project validation detects any graph edge referencing a missing node.
  4. **AT-04-04:** Graph controls and the selected-node detail are usable by keyboard, subject to a separate accessibility audit.
  5. **AT-04-05:** The graph is described as the local question-specific JSON/SVG representation, not a live Neo4j traversal.

- **Trace:** Objective 1 / 4; FR-06, NFR-04; `frontend/app.js`, `data/curated/questions.json`.

---

## Part B — Original personal submission by Zhang Zijian (50106035), reproduced without editing

**Archived source:** `sources/zhang_50106035_use_cases_original.md`  
**Reference:** `https://github.com/xin-315/my-first-github/pull/5/files` (file `reports/add-use-cases-and-rtm-227/use_cases.md`, snapshot commit `9413a58`).

# StudyGraph Personal Use Case Specifications

**Course and Group:** JC2001 / Group 5
**Owner:** 50106035 (Business Analysis)
**Personal scope:** UC-05, UC-06, UC-07 and UC-08
**Document status:** Reviewed personal draft, pending group review
**Internal deadline:** 10 October 2026, 22:00 (Asia/Shanghai)

This document covers only the four use cases assigned to student 50106035.
UC-01 to UC-04 are assigned to 50106038 and are not included here. The
specifications describe the expected system behaviour; they do not claim that
all listed functions have already been implemented.

## 1. Use Case Specification: UC-05 Five-Dimension Learning Analysis

- **Use case ID:** UC-05
- **Use case name:** View the five-dimension learning radar
- **Primary actor:** University student
- **Trigger:** The student opens the learning-analysis page or completes a new attempt.
- **Preconditions:**
  1. The student has opened the system and learning records can be read;
  2. Questions are labelled with the five dimensions: conceptual recall, prerequisite reasoning, misconception recognition, cross-topic reasoning and procedural accuracy.
- **Postconditions:**
  1. The page shows the five-dimension radar, scores and attempt counts;
  2. A successful new attempt updates the related dimensions;
  3. A dimension with too little evidence is labelled “Insufficient evidence”.
- **Main success scenario:**
  1. The student opens the learning-analysis page.
  2. The system reads the attempt records saved in the current browser.
  3. The system counts attempts and correct answers for each dimension.
  4. The system calculates the correct rate for each dimension.
  5. The system displays the radar and the written details.
  6. The student reviews the result and chooses to continue practising or review wrong answers.
- **Extensions and exceptions:**
  - **2a. No attempt records exist:** The system shows an empty state and asks the student to complete a practice question first.
  - **2b. Records cannot be read:** The system shows an error message and does not display the result as 0%.
  - **4a. A dimension has fewer than two attempts:** The system shows “Insufficient evidence” and the current count, without showing a percentage.
- **Special requirements and acceptance criteria:**
  1. After five valid attempts, the radar can refresh using the new results; the page can also be opened with fewer than five attempts;
  2. Dimension score = correct attempts for the dimension / total attempts for the dimension x 100%, rounded for display;
  3. Each question contributes only to its labelled dimensions, and the radar and written details use the same results;
  4. The chart describes practice performance and does not directly prove long-term mastery.

## 2. Use Case Specification: UC-06 Wrong-Answer History

- **Use case ID:** UC-06
- **Use case name:** Find and practise historical wrong answers
- **Primary actor:** University student
- **Trigger:** The student opens the wrong-answer history.
- **Preconditions:**
  1. The system can read the history saved in the current browser;
  2. A history record contains a question ID, subject, attempt time and result; wrong-answer records also contain the misconception.
- **Postconditions:**
  1. The student finds a matching record and views the related question and diagnosis;
  2. A successful retry creates a new record and does not change the original wrong-answer record.
- **Main success scenario:**
  1. The student opens the wrong-answer history.
  2. The system shows wrong attempts by time, with the newest records first.
  3. The student enters a keyword or filters by subject, topic, misconception, result or date.
  4. The system shows the records that satisfy all selected conditions and displays the count.
  5. The student opens one record and views the original question, selected answer and misconception.
  6. The student chooses to retry the question; the system hides the original answer and opens the practice flow.
  7. The student submits a new answer; the system saves the new record and updates the learning evidence.
- **Extensions and exceptions:**
  - **2a. No records exist:** The system shows an empty state and provides a link back to practice.
  - **2b. Records cannot be read:** The system shows an error message and does not change the original records.
  - **4a. No record matches the filters:** The system shows “No matching records” and allows the student to change the filters.
  - **5a. The original question has been removed:** The system keeps the history summary, marks the question as unavailable and disables retry.
- **Special requirements and acceptance criteria:**
  1. Keywords can match the question stem, topic or misconception; English letter case does not affect the search;
  2. “All” results include all valid attempts, and date ranges include both the start and end dates;
  3. Viewing history does not create an attempt, and retrying does not overwrite the original record;
  4. Clearing history requires confirmation; cancelling keeps the data, while confirmation clears the learning records.

## 3. Use Case Specification: UC-07 Adaptive Supplementary Practice

- **Use case ID:** UC-07
- **Use case name:** Recommend supplementary practice for the knowledge point of a wrong answer
- **Primary actor:** University student
- **Trigger:** The student chooses “Practise a similar question” from the diagnosis or learning-analysis page.
- **Preconditions:**
  1. The current wrong answer or a related history record is linked to a knowledge point;
  2. The question set can be searched by knowledge-point labels.
- **Postconditions:**
  1. When a suitable question exists, the student receives a different question for the same knowledge point and a recommendation reason;
  2. After the student completes the recommended question, the new result is added to the learning record.
- **Main success scenario:**
  1. The student chooses “Practise a similar question” from the diagnosis or learning-analysis page.
  2. The system identifies the knowledge point from the current wrong answer or relevant history.
  3. The system searches for questions about the same knowledge point, preferably with a similar difficulty and no previous attempt.
  4. The system displays one question and the reason for the recommendation without showing the answer.
  5. The student accepts the recommendation and enters the normal practice flow.
  6. The system saves the new result and updates the learning evidence.
- **Extensions and exceptions:**
  - **2a. The wrong answer has no knowledge-point label:** The system says that it cannot recommend a question yet and keeps the original diagnosis.
  - **3a. No strict isomorphic variant exists:** The system may recommend an ordinary supplementary question for the same knowledge point, but must label it clearly.
  - **3b. No suitable unattempted question exists:** The system says that no new question is available and allows the student to review an old question.
  - **3c. The question search fails:** The system shows an error and allows the student to continue ordinary practice.
  - **5a. The student rejects the recommendation:** No new attempt is created; the student returns to the diagnosis or ordinary practice.
- **Special requirements and acceptance criteria:**
  1. A recommended question must use the same knowledge point as the original wrong answer and must not be the original question;
  2. An isomorphic variant tests the same knowledge and main method while changing the conditions or wording;
  3. An ordinary question about the same broad topic must not be labelled as an isomorphic variant;
  4. One wrong answer is only a practice signal and does not prove long-term weakness;
  5. The review status of the recommended question must remain visible.

## 4. Use Case Specification: UC-08 Socratic AI Tutor Follow-up

- **Use case ID:** UC-08
- **Use case name:** Ask the AI tutor for a guided question about the current item
- **Primary actor:** University student
- **Trigger:** The student asks a question from the diagnosis or tutor page.
- **Preconditions:**
  1. The current question, hint and explanation evidence have loaded;
  2. The local application service is running; an external model is optional.
- **Postconditions:**
  1. The page shows a guided response related to the current question without directly giving the answer;
  2. The student can ask another question, and tutor messages do not create attempts.
- **Main success scenario:**
  1. The student opens the tutor page and reviews the current question and hint.
  2. The student enters a question such as “Which prerequisite did I miss?”
  3. The system checks the input and reads the current question and related misconception.
  4. The system uses the external model or a local prompt to generate a 2-3 sentence guided response.
  5. The page displays the response and the mode actually used.
  6. The student uses the prompt to explain their reasoning or returns to practice.
- **Extensions and exceptions:**
  - **3a. The input is empty or longer than 1,200 characters:** The system asks the student to edit the input and does not submit it.
  - **4a. The external model is unavailable or times out:** If the local service is available, the system uses a preset local prompt and marks the response as local.
  - **4b. The local application service is also unavailable:** The system shows an error, keeps the question and allows retry.
  - **4c. The student asks for the answer directly:** The tutor gives a question, condition check or counterexample instead of the answer.
  - **5a. The student has moved to another question:** A delayed response for the old question must not appear as a response for the new question.
- **Special requirements and acceptance criteria:**
  1. A normal response contains 2-3 sentences, includes at least one question or thinking prompt, relates to the current question and does not give the answer directly;
  2. The local prompt remains available without an external model;
  3. Viewing the full explanation is a separate action after answering and is not the tutor giving the answer automatically;
  4. Tutor messages do not create learning records.

## 5. Current implementation status

| Use case | Current status |
| --- | --- |
| UC-05 | Basic dimension statistics and the radar exist; full invalid-record handling still needs work |
| UC-06 | Attempts are stored, but the separate history page, filters and retry flow are not complete |
| UC-07 | The recommendation feature has not been implemented |
| UC-08 | Local prompts and model-failure fallback exist; actual misconception-specific follow-up and stale-response handling still need work |

The current PoC uses a Python standard-library service, JSON and SVG. It does not
currently deploy FastAPI, Neo4j or ECharts. This document records the personal
requirements and does not claim that unfinished functions have passed testing.

## 6. Sources

1. `01_requirements_task.md`: personal allocation, use-case template and RTM requirements.
2. `docs/PROJECT_PROPOSAL_DRAFT.md`, Section 4: project objectives.
3. `(Week4)-JC2001-Practical5Exercise-UseCases.pdf`: actors, goals, main steps and exception paths.
4. `server.py`, `frontend/app.js` and `data/curated/questions.json`: current implementation status.
