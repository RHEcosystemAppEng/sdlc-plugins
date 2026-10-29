# Status-Aware Handling Decisions

Per SKILL.md "Status-aware handling" rules, each discovered issue is evaluated
based on its current Jira status to determine the appropriate triage action.

---

## Untriaged Issues (Query 1)

### TC-9001 -- CVE-2026-40112 h2 (Status: New)

**Handling**: Proceed with full triage (default path).

New is the expected starting status for untriaged Vulnerability issues.
No warnings or confirmations needed before beginning the 8-step triage workflow.

---

### TC-9002 -- CVE-2026-40297 serde_json (Status: New)

**Handling**: Proceed with full triage (default path).

New is the expected starting status for untriaged Vulnerability issues.
No warnings or confirmations needed before beginning the 8-step triage workflow.

---

### TC-9003 -- CVE-2026-40455 tokio (Status: In Progress)

**Handling**: Warn the engineer before proceeding.

This issue is already in "In Progress" status. It may be actively worked on.
Per the status-aware handling rules, present the following options to the engineer:

1. **Proceed with triage anyway** -- e.g., to verify version impact or update
   Affects Versions on an issue that is already being remediated.
2. **Skip this issue** -- return to the discovery list or end the session.

Do not begin triage until the engineer confirms their choice.

---

### TC-9004 -- CVE-2026-40518 ring (Status: New)

**Handling**: Proceed with full triage (default path).

New is the expected starting status for untriaged Vulnerability issues.
No warnings or confirmations needed before beginning the 8-step triage workflow.

---

## Triaged but still New (Query 2)

### TC-9010 -- CVE-2026-39874 quinn-proto (Status: New, Label: ai-cve-triaged)

**Handling**: Warn the engineer -- triaged but stale.

This issue carries the `ai-cve-triaged` label (indicating it was previously triaged)
but remains in New status (indicating no remediation action was taken or the issue
was never transitioned). This is flagged as a stale triaged issue.

Options for the engineer:

1. **Re-triage** -- re-run the full triage workflow to verify findings and
   take corrective action (e.g., create missing remediation tasks, transition status).
2. **Skip** -- leave as-is if the prior triage outcome was intentional (e.g.,
   the issue was triaged and found not affected but not yet closed).

---

## Ready for QA Candidates (Query 3)

### TC-9020 -- CVE-2026-38901 hyper (Status: Modified)

**Handling**: Candidate for ON_QA transition.

All linked remediation Tasks are completed:
- TC-9021: Done
- TC-9022: Closed

Since all remediation work is finished, this issue is ready for QA verification.
Recommend: consider transitioning TC-9020 to ON_QA.

---

### TC-9023 -- CVE-2026-39102 rustls (Status: In Progress)

**Handling**: Not ready for QA -- remediation still in progress.

Linked remediation Task status:
- TC-9024: Done
- TC-9025: In Progress (still open)

At least one remediation Task (TC-9025) is still in progress. This issue cannot
move to QA until all linked remediation Tasks are completed.

If the engineer selects this issue for direct triage, the In Progress status
triggers the same warning as TC-9003 above: "This issue is already in In Progress.
It may be actively worked on." Offer to proceed or skip.

---

### TC-9026 -- CVE-2026-39330 openssl (Status: Modified)

**Handling**: Not ready for QA -- no remediation tasks linked.

This issue has no linked Tasks with Depend link type. Without remediation tasks
to verify, it cannot be evaluated for QA readiness. It is excluded from the
Ready for QA list.

If the engineer selects this issue for direct triage, it would proceed as a
normal triage since Modified is not one of the terminal statuses (Closed/Done/Resolved)
but it is also not New. Per the status-aware handling rules, Modified falls under
the "In Progress / Code Review / QA" warning category: warn the engineer that
the issue may be actively worked on and offer to proceed or skip.
