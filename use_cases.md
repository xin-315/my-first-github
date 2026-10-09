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
