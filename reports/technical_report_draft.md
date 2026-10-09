**JC2001: Introduction to Software Engineering**

**Technical Report — M2.1 Working Draft**

**To Design and Implement a Smart Study Assistant System for University Students**

Project: Smart Study Assistant

Group: Group 5

Programme of Study: BSc (BMIS)

Current milestone: Report skeleton + Chapter 1 draft

Report Lead: Xie Weixin (50106034)

| Group Member | Student ID | Role |
| --- | --- | --- |
| Wu Yuxuan        | 50106070       | Group Lead                                  |
| Xie Weixin       | 50106034       | Report Lead                                 |
| Lin Yongtong     | 50106038       | Requirements Lead                           |
| Zhang Zijian     | 50106035       | Business Analysis                           |
| Wang Sijian      | 50106045       | System Architect                            |
| Xi Yusai         | 50105989       | UI/UX Design                                |
| Jiang Hao        | 50106065       | Architecture Task Reviewer                  |
| Yang Mingjie     | 50106061       | Software Testing Lead                       |
| Liang Zixuan     | 50106037       | Presentation / Media / Deployment Lead      |
| Dong Siqin       | 50106060       | PoC Logic Developer — Diagnostic API & Quiz |

# Table of Contents

- [List of Figures](#list-of-figures)
- [List of Tables](#list-of-tables)
- [Current Milestone Scope](#current-milestone-scope)
- [1. Introduction and Project Context](#1-introduction-and-project-context)
  - [1.1 Background and Motivation](#11-background-and-motivation)
  - [1.2 Problem Definition](#12-problem-definition)
  - [1.3 Proposed Solution and Main Features](#13-proposed-solution-and-main-features)
  - [1.4 Project Objectives](#14-project-objectives)
  - [1.5 Intended Users and Stakeholders](#15-intended-users-and-stakeholders)
  - [1.6 Scope, Assumptions and Boundaries](#16-scope-assumptions-and-boundaries)
  - [1.7 Expected Value and Evaluation Approach](#17-expected-value-and-evaluation-approach)
  - [1.8 Report Structure](#18-report-structure)
  - [1.9 Chapter Summary](#19-chapter-summary)
- [2. Functional and Non-Functional Requirements](#2-functional-and-non-functional-requirements)
  - [2.1 Functional Requirements](#21-functional-requirements)
  - [2.2 Non-Functional Requirements](#22-non-functional-requirements)
  - [2.3 Acceptance Criteria and Requirements Traceability](#23-acceptance-criteria-and-requirements-traceability)
- [3. Use Cases and Requirements Modelling](#3-use-cases-and-requirements-modelling)
  - [3.1 Actors and System Boundary](#31-actors-and-system-boundary)
  - [3.2 Use-Case Diagram](#32-use-case-diagram)
  - [3.3 Key Use-Case Descriptions](#33-key-use-case-descriptions)
- [4. System Design and Architecture](#4-system-design-and-architecture)
  - [4.1 Architecture Overview](#41-architecture-overview)
  - [4.2 Components and Relationships](#42-components-and-relationships)
  - [4.3 Relevant Models and Design Decisions](#43-relevant-models-and-design-decisions)
- [5. Implementation](#5-implementation)
  - [5.1 Implemented PoC Scope](#51-implemented-poc-scope)
  - [5.2 Technologies, Tools and Software Structure](#52-technologies-tools-and-software-structure)
  - [5.3 Algorithms and User Interface](#53-algorithms-and-user-interface)
- [6. Testing and Evaluation](#6-testing-and-evaluation)
  - [6.1 Test Strategy and Test Cases](#61-test-strategy-and-test-cases)
  - [6.2 Test Methods and Results](#62-test-methods-and-results)
  - [6.3 Evaluation Against Requirements](#63-evaluation-against-requirements)
- [7. Conclusions and Future Work](#7-conclusions-and-future-work)
  - [7.1 Project Outcomes and Objective Achievement](#71-project-outcomes-and-objective-achievement)
  - [7.2 Limitations](#72-limitations)
  - [7.3 Future Work](#73-future-work)
- [References](#references)
- [Appendix A – Group Workload Profile](#appendix-a--group-workload-profile)
# List of Figures

No final figure captions have been added yet; update this list when figures are approved.

# List of Tables

No final table captions have been added yet; update this list when tables are approved.

# Current Milestone Scope

Current deliverable: report skeleton plus a draft of Chapter 1. Chapters 2–7 are outline placeholders only. The separate draft black-box test matrix at the end is for the testing team to review and finalise.

# 1. Introduction and Project Context

## 1.1 Background and Motivation

University students often revise for examinations using a mixture of lecture slides, textbook chapters, tutorial sheets and online materials. Although these sources contain useful information, their concepts are distributed across separate documents and are not always connected explicitly. Students therefore need to spend time locating definitions, reconstructing prerequisite relationships and deciding which topics to review. The challenge is not simply a lack of learning materials, but the effort required to turn fragmented information into an organised understanding that can be applied to unfamiliar questions.

Conventional practice tools can indicate whether an answer is correct, but a binary result or a standard answer explanation may not explain why a particular incorrect option was attractive. Students may repeat the same mistakes when underlying misconceptions, missing prerequisite knowledge or invalid assumptions remain unidentified. This is particularly relevant in subjects requiring multi-step reasoning, rule application, quantitative work or interpretation of conceptual boundaries. An effective revision workflow should connect an answer choice with an explanation of the likely reasoning error and a practical next step.

Generative artificial intelligence (AI) can provide explanations in natural language, but its responses need to be grounded in relevant learning content. The Smart Study Assistant combines retrieval-augmented generation (RAG) with a structured knowledge graph to support more context-aware learning feedback. The knowledge graph organises concepts, prerequisite conditions, operational steps and common misconceptions. A language model then helps formulate diagnostic explanations and follow-up prompts based on the retrieved information. This approach aims to make learning support more structured, explainable and relevant to the material being studied \[1\], \[2\], \[3\].

## 1.2 Problem Definition

The project addresses four related problems. First, learning resources are fragmented, increasing the time and effort needed to establish connections between concepts. Second, repeated practice may measure answer selection without revealing the misconception behind an error. Third, students may have limited visibility into their strengths and weaknesses across different types of cognitive activity. Fourth, generative AI responses can contain unsupported statements, which may reinforce misunderstandings rather than correct them.

The central engineering question is whether a proof-of-concept system can connect question practice, diagnostic feedback, concept exploration and targeted follow-up activities within a single workflow. In particular, the system is designed to transform a student's selected answer into a structured learning response by combining a web interface, an API service, knowledge-graph retrieval and an external language-model service. The project therefore focuses on integrating these components into a coherent study-support process.

## 1.3 Proposed Solution and Main Features

The Smart Study Assistant is designed as a browser-based learning support system, using a single-page application (SPA) connected to a Python/FastAPI service. Its planned architecture uses Neo4j AuraDB to store the knowledge graph and the Qwen-Turbo language model through the DashScope API to support diagnostic explanations and conversational assistance.

The main workflow begins when a student opens a question and selects an answer. When the answer is incorrect, the system is designed to initiate a diagnostic process, retrieve relevant concepts or misconception relationships, and present an explanation with a suggested next step. Students can then explore related concepts, review previous mistakes, inspect a five-dimensional mastery visualisation, practise a related variant question or ask a focused follow-up question through the tutoring interface.

The knowledge graph organises learning content into several categories: core concepts, prerequisite conditions, misconception or trap concepts, and operational steps. Relationships between these elements may represent prerequisites, logical derivations, calculation steps and associations with common errors. These relationships provide structured context for retrieving relevant learning information and generating more targeted feedback.

The main features are intended to work together as a connected revision workflow rather than as isolated tools. The system brings question practice, error diagnosis, concept navigation, progress visualisation and follow-up learning activities into one interface.

## 1.4 Project Objectives

The project has five SMART objectives, with the planned completion date of 14 December 2026.

**Objective 1 — Functional proof-of-concept delivery.** By 14 December 2026, design, develop, test and package a runnable Smart Study Assistant proof of concept integrating Neo4j cloud storage, Qwen-Turbo diagnostics, Socratic tutoring and ECharts 5.5.1 visualisation.

**Objective 2 — Knowledge graph scale and query latency.** Construct a knowledge graph containing at least 250 concept nodes, 500 examination questions and 300 explicit misconception relationships. Keep bidirectional Cypher traversal at a depth of two or less, with a LIMIT 40 query completing in under 2.0 seconds.

**Objective 3 — Diagnostic precision and noise reduction.** Achieve at least 85% diagnostic extraction accuracy on examination distractors. Apply a confidence threshold of 85 to filter at least 85% of spurious graph relationships, while using graph-grounded information to reduce unsupported AI guidance.

**Objective 4 — Software quality and test coverage.** Use modular object-oriented design, achieve 100% unit-test coverage for core Cypher wrappers, achieve at least 80% branch coverage for diagnostic logic using pytest, prevent unhandled HTTP 429 exceptions, and comply with PEP 8 conventions.

**Objective 5 — Documentation and submission compliance.** By 14 December 2026 at 23:59 China Standard Time, prepare and submit the 40–60 page technical report without raw source code, an 8–12 page user manual in PDF format, a 15-minute presentation video with slides, and Appendix A containing the signed Group Workload Profile.

Together, these objectives define the intended scope of the proof of concept, its technical targets, software quality expectations and required documentation.

## 1.5 Intended Users and Stakeholders

The primary intended users are university students preparing for examinations in concept-heavy or structured subjects. Relevant examples include students studying computing, business or management, and engineering-related subjects. The system is intended to support individual revision by helping students understand errors, explore related concepts and decide what to practise next. It is not intended to replace lectures, instructors, official learning resources or academic judgement.

Secondary stakeholders include teaching assistants and instructors. They may benefit from reusable diagnostic question content and a clearer view of recurring misconceptions, particularly where the system supports the review of common errors. The project team is also an important stakeholder because development requires coordination across requirements modelling, interface design, graph architecture, API integration, testing, deployment and documentation. Clear interfaces and traceable requirements help these activities work together consistently.

## 1.6 Scope, Assumptions and Boundaries

The project focuses on a course-level proof of concept demonstrating the feasibility of a knowledge-graph-grounded study workflow. Its technical scope includes question practice, diagnostic feedback, concept retrieval, knowledge-graph exploration, learning-progress visualisation and related follow-up activities, subject to the agreed implementation scope.

The project includes measurable targets for graph size, retrieval latency, diagnostic extraction accuracy, test coverage, software packaging and documentation. It is not intended to be a production learning-management system, a replacement for a university's official learning platform, or a validated measure of a student's overall intelligence or academic potential.

The system design assumes that suitable question content and concept relationships can be prepared, that the external language-model API is available within its service limits, and that the knowledge graph and development environment can be configured successfully. Potential constraints include API rate limits, network failures, incomplete graph coverage, variability in model output, limited proof-of-concept data and the time available for development. These factors inform the design priorities and the scope of evaluation.

## 1.7 Expected Value and Evaluation Approach

The expected value for students is more informative feedback after an incorrect answer, clearer navigation between related concepts and more actionable guidance about what to revise next. The mastery visualisation is intended to summarise recorded practice patterns across five dimensions: Basic Recall, Boundary Deduction, Trap Defense, Cross-Topic Synthesis and Calculation Precision. These dimensions provide learning-support indicators based on recorded activity rather than definitive measurements of a student's overall ability.

The system will be evaluated through requirements traceability and evidence-based testing. Functional requirements will be linked to project objectives, use cases and acceptance tests. Non-functional requirements, including response time, reliability and test coverage, will be assessed using defined test conditions and recorded measurements. The evaluation will compare observed results with the objectives and acceptance criteria, identifying areas of achievement and aspects requiring further improvement.

Where learning efficiency, diagnostic accuracy or the reduction of unsupported responses is evaluated, the assessment will use an appropriate dataset, a repeatable procedure and documented results. This approach supports a consistent evaluation of system behaviour and technical performance.

## 1.8 Report Structure

The technical report is organised into seven main chapters. Chapter 1 introduces the project context, problem, objectives, intended users, proposed solution and scope. Chapter 2 specifies the functional and non-functional requirements. Chapter 3 presents the use cases and requirements models. Chapter 4 describes the system design and architecture. Chapter 5 explains the proof-of-concept implementation, including the technologies, software structure, algorithms and interface. Chapter 6 presents the testing methods, results and evaluation against the requirements. Chapter 7 summarises the project outcomes, limitations and future work.

The main body is followed by the references and Appendix A, which contains the Group Workload Profile.

## 1.9 Chapter Summary

This chapter has introduced the learning problems addressed by the Smart Study Assistant, the proposed knowledge-graph-grounded approach, the project objectives, the intended users and the expected value. It has also defined the project scope and outlined how the system will be evaluated. These elements provide the foundation for specifying measurable requirements and connecting them to use cases, architecture, implementation and testing in the subsequent chapters.

# M2.1 Status Note — remove before final submission

This is an interim working draft. The current task is to provide a report skeleton and a draft of Chapter 1. Chapters 2–7 below are headings only, with prompts to guide later work. They are not completed report content.

# 2. Functional and Non-Functional Requirements

## 2.1 Functional Requirements

*\[To be completed in a later milestone. Do not treat this section as completed content.\]*

## 2.2 Non-Functional Requirements

*\[To be completed in a later milestone. Do not treat this section as completed content.\]*

## 2.3 Acceptance Criteria and Requirements Traceability

*\[To be completed in a later milestone. Do not treat this section as completed content.\]*

# 3. Use Cases and Requirements Modelling

## 3.1 Actors and System Boundary

*\[To be completed in a later milestone. Do not treat this section as completed content.\]*

## 3.2 Use-Case Diagram

*\[To be completed in a later milestone. Do not treat this section as completed content.\]*

## 3.3 Key Use-Case Descriptions

*\[To be completed in a later milestone. Do not treat this section as completed content.\]*

# 4. System Design and Architecture

## 4.1 Architecture Overview

*\[To be completed in a later milestone. Do not treat this section as completed content.\]*

## 4.2 Components and Relationships

*\[To be completed in a later milestone. Do not treat this section as completed content.\]*

## 4.3 Relevant Models and Design Decisions

*\[To be completed in a later milestone. Do not treat this section as completed content.\]*

# 5. Implementation

## 5.1 Implemented PoC Scope

*\[To be completed in a later milestone. Do not treat this section as completed content.\]*

## 5.2 Technologies, Tools and Software Structure

*\[To be completed in a later milestone. Do not treat this section as completed content.\]*

## 5.3 Algorithms and User Interface

*\[To be completed in a later milestone. Do not treat this section as completed content.\]*

# 6. Testing and Evaluation

## 6.1 Test Strategy and Test Cases

*\[To be completed in a later milestone. Do not treat this section as completed content.\]*

## 6.2 Test Methods and Results

*\[To be completed in a later milestone. Do not treat this section as completed content.\]*

## 6.3 Evaluation Against Requirements

*\[To be completed in a later milestone. Do not treat this section as completed content.\]*

# 7. Conclusions and Future Work

## 7.1 Project Outcomes and Objective Achievement

*\[To be completed in a later milestone. Do not treat this section as completed content.\]*

## 7.2 Limitations

*\[To be completed in a later milestone. Do not treat this section as completed content.\]*

## 7.3 Future Work

*\[To be completed in a later milestone. Do not treat this section as completed content.\]*

# References

\[1\] P. Lewis et al., "Retrieval-augmented generation for knowledge-intensive NLP tasks," in NeurIPS, vol. 33, pp. 9459–9474, 2020.

\[2\] D. Edge et al., "From local to global: A graph rag approach to query-focused summarization," arXiv:2404.16130, 2024.

\[3\] I. Robinson, J. Webber, and E. Eifrem, Graph Databases: New Opportunities for Connected Data, 2nd ed. Sebastopol, CA: O'Reilly, 2015.

***\[Add and verify sources actually cited in the report during later drafting.\]***

# Appendix A – Group Workload Profile

*\[Insert the official Group Workload Profile template from MyAberdeen after the group has completed and agreed it.\]*
