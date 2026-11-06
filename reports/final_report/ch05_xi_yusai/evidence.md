# Chapter 5.5 Evidence & Source Anchors

**Author:** Xi Yusai (50105989)
**Section:** Graphical User Interface (5.5.1 – 5.5.4)

## 1. Code Reference Anchors
All implementation descriptions in this chapter are traceable to the following repository files.

| File Path | Corresponding Section | Core Content Referenced |
| :--- | :--- | :--- |
| `frontend/index.html` | 5.5.1.1, 5.5.2 | Global console layout structure, page module hierarchy |
| `frontend/app.js` | 5.5.2.1, 5.5.2.2 | Theme switching logic, component state control, interaction behaviour |
| `frontend/style.css` | 5.5.1.2, 5.5.3.1 | CSS variable system, dual-theme rules, responsive style breakpoints |

## 2. Design Document Anchors
All design decisions are derived from the pre-defined UI specification, no subjective additions.

| File Path | Corresponding Section | Core Content Referenced |
| :--- | :--- | :--- |
| `reports/ui-design/02-design-system.md` | 5.5.1.2, 5.5.1.3 | Colour tokens, 8px grid system, typography specification, component rules |
| `reports/ui-design/04-interaction-spec.md` | 5.5.2 | Full interaction flow, state transition rules, exception handling logic |
| `reports/ui-design/05-checklist.md` | 5.5.3.3 | UI restoration acceptance dimensions, review workflow and criteria |

## 3. Requirement Alignment Mapping
All design and implementation items strictly correspond to the group Requirements Traceability Matrix.

| Requirement ID | Corresponding Section | Description of Alignment |
| :--- | :--- | :--- |
| FR-04 | 5.5.2.4 | Five-dimension mastery radar visualisation and evidence insufficiency label |
| FR-08 | 5.5.2.3 | Question evidence, source and review status display in Trap Drawer |
| FR-09 | 5.5.2.2 | Collapsible hint and explanation; viewing hint does not create an attempt |
| NFR-03 | 5.5.1.2, 5.5.3.2 | Light/dark dual theme; icon+text dual status indication; WCAG compliance |
| NFR-07 | 5.5.2.4 | Radar shows attempt count; "Insufficient evidence" label for low-data dimensions |
| NFR-08 | 5.5.3.1 | Desktop-first responsive adaptation, core functions available on mobile |

## 4. Figure Sources
| Figure ID | Description |
| :--- | :--- |
| Fig 5.3 | Split-Screen Five-Layer Trap Drawer Architecture diagram |
| Fig 5.4 | Panoramic layout overview of the student-side main console |
| Fig 5.5 | Five-axis competency mastery radar schematic |
