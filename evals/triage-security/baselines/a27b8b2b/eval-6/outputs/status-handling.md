# Status-Aware Handling Decisions

This document details the status-aware handling applied to each issue discovered
in the three JQL queries, following the status-aware handling protocol from the
triage-security skill.

---

## Query 1: Untriaged Issues

### TC-9001 — Status: New

- **Handling**: Proceed with full triage (default path).
- **Action**: This issue is in New status, which is the expected starting state for
  untriaged Vulnerability issues. Full triage (Steps 0 through 8) can proceed
  without any warnings or additional confirmation.

### TC-9002 — Status: New

- **Handling**: Proceed with full triage (default path).
- **Action**: This issue is in New status. Full triage can proceed without any
  warnings or additional confirmation.

### TC-9003 — Status: In Progress

- **Handling**: Warning — active work detected.
- **Action**: This issue is already in **In Progress** status. It may be actively
  worked on by another engineer.

  > "This issue is already in `In Progress`. It may be actively worked on."

  The engineer is presented with two options:
  1. **Proceed with triage anyway** — e.g., to verify version impact or update
     Affects Versions even though work has already started.
  2. **Skip this issue** — return to the discovery list or end the session.

  Triage does NOT proceed automatically for In Progress issues. Explicit
  confirmation is required before any Steps execute.

### TC-9004 — Status: New

- **Handling**: Proceed with full triage (default path).
- **Action**: This issue is in New status. Full triage can proceed without any
  warnings or additional confirmation.

---

## Query 2: Triaged but still New

### TC-9010 — Status: New (with ai-cve-triaged label)

- **Handling**: Flagged as stale — triaged but never actioned.
- **Action**: This issue carries the `ai-cve-triaged` label (indicating it was
  previously triaged) but remains in New status, meaning no triage actions were
  ever executed or the triage outcome was not acted upon.

  Recommended follow-up:
  - Re-triage to verify the original version impact assessment is still valid
    (dependency versions may have changed since the original triage)
  - Or manually transition to the appropriate status if the original triage
    outcome was valid but never executed

  If selected for re-triage, the New status allows full triage to proceed
  without the In Progress / Closed warnings.

---

## Query 3: Ready for QA Candidates

### TC-9020 — Status: Modified

- **Handling**: Ready for QA transition.
- **Action**: All linked remediation Tasks are completed:
  - TC-9021: **Done**
  - TC-9022: **Closed**

  Since all remediation work is complete, this issue is a candidate for
  transition to **ON_QA** status. The engineer should verify that the
  remediation tasks addressed all affected versions before transitioning.

  Proposed action: Transition TC-9020 to ON_QA.

### TC-9023 — Status: In Progress

- **Handling**: Excluded from Ready for QA — remediation incomplete.
- **Action**: Linked remediation Tasks are not all completed:
  - TC-9024: **Done** (completed)
  - TC-9025: **In Progress** (still active)

  TC-9025 is still being worked on. This issue cannot transition to ON_QA
  until all linked remediation Tasks reach Done or Closed status.

  No action proposed. This issue will become Ready for QA once TC-9025
  is completed.

### TC-9026 — Status: Modified

- **Handling**: Excluded from Ready for QA — no remediation tasks linked.
- **Action**: This issue has no linked Tasks with type "Depend". Without
  linked remediation tasks, there is no remediation work to verify completion of.

  This may indicate:
  - The triage concluded with Case C (no supported versions affected) and
    the issue should have been closed
  - Remediation tasks were created but not linked properly
  - The triage was interrupted before Step 8 (Remediation) completed

  The engineer should investigate why no remediation tasks are linked
  before taking action on this issue.
