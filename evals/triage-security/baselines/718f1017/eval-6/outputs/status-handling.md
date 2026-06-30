# Status-Aware Handling Decisions

This document describes the status-aware handling decisions for each issue listed in discovery mode, following the triage-security methodology (SKILL.md, "Status-aware handling" section under Discovery Mode).

The methodology defines three handling paths based on an issue's current Jira status:

- **New** -- proceed with full triage (default path)
- **In Progress / Code Review / QA** -- warn: "This issue is already in `<status>`. It may be actively worked on." Ask whether to (1) proceed with triage anyway, or (2) skip this issue.
- **Closed / Done / Resolved** -- warn: "This issue is already closed." Ask whether to (1) re-triage, or (2) skip this issue.

---

## Untriaged Issues (Query 1)

### TC-9001 -- CVE-2026-40112 h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2]
- **Status:** New
- **Handling:** Proceed with full triage (default path). No warning needed. This is a standard untriaged issue ready for version impact analysis, Affects Versions correction, duplicate/sibling detection, lifecycle check, already-fixed check, and remediation task creation.

### TC-9002 -- CVE-2026-40297 serde_json - Stack overflow on deeply nested input [rhtpa-2.1]
- **Status:** New
- **Handling:** Proceed with full triage (default path). No warning needed. Standard untriaged issue following the full 7-step triage sequence.

### TC-9003 -- CVE-2026-40455 tokio - Race condition in task cancellation [rhtpa-2.2]
- **Status:** In Progress
- **Handling:** This issue is already in `In Progress`. It may be actively worked on. Before proceeding, the engineer must be warned:

  > "This issue is already in `In Progress`. It may be actively worked on."

  The engineer is asked whether to:
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue

  If the engineer chooses to skip, return to the discovery list or end the session.

### TC-9004 -- CVE-2026-40518 ring - Timing side-channel in RSA verification [rhtpa-2.2]
- **Status:** New
- **Handling:** Proceed with full triage (default path). No warning needed. Standard untriaged issue following the full 7-step triage sequence.

---

## Triaged but still New (Query 2)

### TC-9010 -- CVE-2026-39874 quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2]
- **Status:** New
- **Handling:** Proceed with full triage (default path). No warning needed based on status alone. However, this issue carries the `ai-cve-triaged` label, meaning it was previously triaged but never moved out of New status. This signals a potential stale issue that may need follow-up or re-triage. The engineer should be informed:

  > "This issue was previously triaged (has `ai-cve-triaged` label) but remains in New status. It may need follow-up or re-triage."

  If selected for triage, the full 7-step process runs as normal (the `ai-cve-triaged` label does not alter the triage flow -- it is an informational marker).

---

## Ready for QA Candidates (Query 3)

### TC-9020 -- CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]
- **Status:** Modified
- **Linked Tasks:** TC-9021 (Done), TC-9022 (Closed)
- **Handling:** All linked remediation Tasks (link type "Depend") are completed (Done or Closed). This issue qualifies as **Ready for QA**. If selected, the recommendation is to transition to ON_QA status.

  Since the status is Modified (not New, not In Progress/Code Review/QA, not Closed/Done/Resolved), it does not trigger a skip or re-triage warning. The Modified status indicates post-triage work has been done, consistent with a QA transition.

### TC-9023 -- CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]
- **Status:** In Progress
- **Linked Tasks:** TC-9024 (Done), TC-9025 (In Progress)
- **Handling:** Excluded from Ready for QA because TC-9025 is still In Progress -- remediation is not yet complete. If the engineer selects this issue for triage, the In Progress status warning applies:

  > "This issue is already in `In Progress`. It may be actively worked on."

  The engineer is asked whether to:
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue

### TC-9026 -- CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]
- **Status:** Modified
- **Linked Tasks:** None (no Depend-linked tasks)
- **Handling:** Excluded from Ready for QA because there are no linked remediation Tasks with link type "Depend". Without remediation tasks, there is nothing to verify for QA. If the engineer selects this issue, its Modified status does not trigger a skip or re-triage warning. Full triage may reveal that remediation tasks need to be created or that the issue was handled through a different mechanism.

---

## Summary of Status-Aware Decisions

| Issue | Status | ai-cve-triaged | Handling Decision |
|-------|--------|----------------|-------------------|
| TC-9001 | New | No | Full triage -- default path |
| TC-9002 | New | No | Full triage -- default path |
| TC-9003 | In Progress | No | Warn: may be actively worked on. Ask to proceed or skip |
| TC-9004 | New | No | Full triage -- default path |
| TC-9010 | New | Yes | Full triage -- flag as previously triaged but stale |
| TC-9020 | Modified | Yes | Ready for QA -- recommend ON_QA transition |
| TC-9023 | In Progress | Yes | Excluded from QA (tasks in progress). Warn if selected |
| TC-9026 | Modified | Yes | Excluded from QA (no Depend tasks). Triage if selected |
