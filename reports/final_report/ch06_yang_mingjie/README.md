# Chapter 6 delivery

Author: Mingjie Yang, 50106061. Primary existing software: sync/cycle3-final ae7ab47.

- outline.md: chapter structure and material inventory.
- draft.md: complete English chapter, five numbered table groups and two figures.
- chapter6_testing_evaluation.pdf: readable formatted chapter; final integration must retain the identified source version.
- appendix_C_test_inventory.pdf and appendix_C.md: test evidence summary. Full electronic inventory: evidence/cycle3/test_case_inventory.csv, all 183 cases.
- user_manual.pdf and user_manual.md: ten-page manual for the existing Cycle 3 application, including screenshots and actual limitations.
- sources.md: Harvard references and primary-source provenance.
- requirement_crosswalk.md: preserves original task wording and records conflicts with the current Ch2 draft.
- peer_review.md: written review of architecture quality claims and Ch6.5 alignment.
- viva_qa.md: five-minute explanation and questions in Chinese.
- evidence/: actual run outputs, hashes, request observations and browser verification. Network guard is an audit helper, not a product feature.

The report does not assert RAGAS scores, novice acceptance, complete offline operation, secure authentication or live learner telemetry. Those claims are not supported by the current software. Review and resolve the listed integration issues with the report lead before the course submission. Academic authorship and AI-use disclosure remain the student's responsibility under the official brief.

No source code is embedded in the report PDF. Browser screenshots show the existing application. Credential values, the application's existing sensitive configuration, installed dependencies and full software archives are excluded from this report-only package.

The chapter has eight main pages plus one reference page. It uses A4, one-inch margins, 12-point Times New Roman and 18-point line spacing. Original Chinese requirement labels use an embedded 12-point SimSun fallback so that they can be quoted verbatim in Table 6.5. Third-level headings are bold run-in headings in the PDF and separate Markdown headings in the editable draft. Figure 6.2 shares rows with Table 6.3; a separate SVG is supplied. English label translations and the later Ch2 assessment are in requirement_crosswalk.md, also embedded in the appendix. Tables C.1 and C.2 formally assess all ten assigned NFRs and all ten later-draft quality requirements. The review is also placed under the required sibling reviews/ directory.

See acceptance_checklist.md and the root PERSONAL_TASK_AUDIT_zh.md for this contributor's completed files and remaining personal actions. The live-run image records a real local test subprocess, with separate verification logs. Human manual acceptance and viva rehearsal remain unperformed. Team software repair, other chapters, whole-report assembly and course submission are outside this personal contribution.

Live GitHub recheck on 29 October 2026: latest master is 7d29bad. Among 296 original files, only backend/run.py changed; the test sources, API, frontend, requirements, assigned task packs and MMLU data are unchanged. Historical execution records remain attributed to ae7ab47. The former sync/cycle3-final branch has been removed and develop is absent. Use the updated root SUBMISSION_GUIDE_zh.md for personal submission; evidence/github_recheck.json records the source comparison. The manual's download instructions now use the available master branch. Newly added group test-plan statuses and the group software ZIP have not been counted as personal execution evidence.

The group ZIP was inspected by file hashes and archive inventory: eight current auth/report files are missing and twelve other application/test files differ. It was not executed. The manual targets the tested repository source and explicitly records this package mismatch; source/package alignment remains with the software package owner.
