# Status-Aware Handling Decisions

For each issue listed in the discovery results, the following status-aware handling
applies per the SKILL.md Status-aware handling protocol.

---

## Untriaged Issues (Query 1)

### TC-9001 — Status: New

**Handling**: Proceed with full triage (default path).

New issues follow the standard triage flow: Step 1 (Data Extraction) through
Step 8 (Remediation). No warning or confirmation needed before starting.

- CVE: CVE-2026-40112
- Stream: rhtpa-2.2 (from suffix `[rhtpa-2.2]`)
- Action: Full triage available

---

### TC-9002 — Status: New

**Handling**: Proceed with full triage (default path).

New issues follow the standard triage flow: Step 1 (Data Extraction) through
Step 8 (Remediation). No warning or confirmation needed before starting.

- CVE: CVE-2026-40297
- Stream: rhtpa-2.1 (from suffix `[rhtpa-2.1]`)
- Action: Full triage available

---

### TC-9003 — Status: In Progress

**Handling**: Warning — this issue is already in `In Progress`. It may be actively worked on.

Before proceeding with triage, the engineer must choose:

1. **Proceed with triage anyway** — e.g., to verify version impact or update Affects Versions
2. **Skip this issue** — return to the discovery list or end the session

This warning is triggered because the issue has progressed beyond New, indicating
that an engineer may already be working on it. Triaging could produce conflicting
or redundant actions.

- CVE: CVE-2026-40455
- Stream: rhtpa-2.2 (from suffix `[rhtpa-2.2]`)
- Action: Requires engineer decision before proceeding

---

### TC-9004 — Status: New

**Handling**: Proceed with full triage (default path).

New issues follow the standard triage flow: Step 1 (Data Extraction) through
Step 8 (Remediation). No warning or confirmation needed before starting.

- CVE: CVE-2026-40518
- Stream: rhtpa-2.2 (from suffix `[rhtpa-2.2]`)
- Action: Full triage available

---

## Triaged but still New (Query 2)

### TC-9010 — Status: New (triaged)

**Handling**: Proceed with full triage (default path for New status).

Although this issue has the `ai-cve-triaged` label (indicating it was previously
triaged), its status remains New. This suggests triage was completed but no
follow-up actions were taken (no status transition, no remediation tasks created,
or tasks were created but the issue was not moved to In Progress). The engineer
should review whether re-triage is needed or if the existing triage results are
still valid.

- CVE: CVE-2026-39874
- Stream: rhtpa-2.2 (from suffix `[rhtpa-2.2]`)
- Action: Full triage available; consider reviewing prior triage results first

---

## Ready for QA (Query 3)

### TC-9020 — Status: Modified

**Handling**: All linked remediation Tasks are completed.

This issue has two linked remediation Tasks via "Depend" links:
- TC-9021: **Done**
- TC-9022: **Closed**

Both tasks are in terminal states, meaning all remediation work is complete.
This issue is a candidate for transitioning to ON_QA.

- CVE: CVE-2026-38901
- Stream: rhtpa-2.2 (from suffix `[rhtpa-2.2]`)
- Action: Consider transitioning to ON_QA

---

### TC-9023 — Status: In Progress

**Handling**: Remediation still in progress — NOT ready for QA.

This issue has two linked remediation Tasks via "Depend" links:
- TC-9024: **Done**
- TC-9025: **In Progress**

TC-9025 is still being worked on. The issue cannot move to QA until all
remediation tasks are complete.

- CVE: CVE-2026-39102
- Stream: rhtpa-2.1 (from suffix `[rhtpa-2.1]`)
- Action: Wait for TC-9025 to complete before considering ON_QA transition

---

### TC-9026 — Status: Modified

**Handling**: No remediation tasks linked — NOT ready for QA.

This issue has no linked Tasks with link type "Depend". Without remediation
tasks, there is nothing to verify in QA. This may indicate:
- Remediation tasks were never created (triage may have been incomplete)
- The issue was triaged as "not affected" but not closed
- Tasks were created but not linked properly

- CVE: CVE-2026-39330
- Stream: rhtpa-2.2 (from suffix `[rhtpa-2.2]`)
- Action: Investigate why no remediation tasks are linked; may need re-triage
