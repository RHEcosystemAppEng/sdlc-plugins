# Status-Aware Handling Decisions

When the engineer selects an issue from the discovery listing (or when a specific
issue key is provided), the skill checks the current Jira status and adapts the
triage workflow accordingly. The rules below are applied per the SKILL.md
status-aware handling protocol.

## Status Handling Rules

| Status | Action |
|--------|--------|
| **New** | Proceed with full triage (Steps 0.7 through 8) -- default path |
| **In Progress / Code Review / QA** | Warn: "This issue is already in `<status>`. It may be actively worked on." Offer: (1) Proceed with triage anyway, (2) Skip this issue |
| **Closed / Done / Resolved** | Warn: "This issue is already closed." Offer: (1) Re-triage to verify fix coverage, (2) Skip this issue |
| **Modified** | Not a terminal or in-progress status in the standard vulnerability workflow; proceed with triage, noting the current status |

---

## Per-Issue Handling Decisions

### Query 1: Untriaged Issues

#### TC-9001 -- CVE-2026-40112 (h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2])

- **Current status:** New
- **Handling:** Proceed with full triage. This is the default path -- assign to current user, transition to Assigned, and execute Steps 1 through 8.
- **Stream scope:** rhtpa-2.2 maps to stream 2.2.x

#### TC-9002 -- CVE-2026-40297 (serde_json - Stack overflow on deeply nested input [rhtpa-2.1])

- **Current status:** New
- **Handling:** Proceed with full triage. This is the default path -- assign to current user, transition to Assigned, and execute Steps 1 through 8.
- **Stream scope:** rhtpa-2.1 maps to stream 2.1.x

#### TC-9003 -- CVE-2026-40455 (tokio - Race condition in task cancellation [rhtpa-2.2])

- **Current status:** In Progress
- **Handling:** Warn the engineer before proceeding.
  - Warning: "This issue is already in `In Progress`. It may be actively worked on."
  - Options presented:
    1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
    2. Skip this issue
  - If the engineer chooses to skip, return to the discovery list.
- **Stream scope:** rhtpa-2.2 maps to stream 2.2.x

#### TC-9004 -- CVE-2026-40518 (ring - Timing side-channel in RSA verification [rhtpa-2.2])

- **Current status:** New
- **Handling:** Proceed with full triage. This is the default path -- assign to current user, transition to Assigned, and execute Steps 1 through 8.
- **Stream scope:** rhtpa-2.2 maps to stream 2.2.x

---

### Query 2: Triaged but still New

#### TC-9010 -- CVE-2026-39874 (quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2])

- **Current status:** New
- **Labels:** ai-cve-triaged (previously triaged)
- **Handling:** Proceed with full triage (status is New, so the default path applies). However, this issue was previously triaged (has the `ai-cve-triaged` label) but never advanced past New status. This is a stale issue that may need:
  - Re-triage to verify that the previous triage assessment is still valid
  - Follow-up to determine why remediation was not started
  - Investigation into whether remediation tasks were created but not linked
- **Stream scope:** rhtpa-2.2 maps to stream 2.2.x

---

### Query 3: Ready for QA Candidates

#### TC-9020 -- CVE-2026-38901 (hyper - HTTP request smuggling [rhtpa-2.2])

- **Current status:** Modified
- **Labels:** ai-cve-triaged
- **Linked Tasks:** TC-9021 (Done), TC-9022 (Closed)
- **Handling:** All linked remediation Tasks are in terminal state. This issue is a candidate for ON_QA transition. The engineer should consider transitioning TC-9020 to ON_QA to advance it through the verification pipeline.
- **Stream scope:** rhtpa-2.2 maps to stream 2.2.x

#### TC-9023 -- CVE-2026-39102 (rustls - Certificate validation bypass [rhtpa-2.1])

- **Current status:** In Progress
- **Labels:** ai-cve-triaged
- **Linked Tasks:** TC-9024 (Done), TC-9025 (In Progress)
- **Handling:** Excluded from Ready for QA. TC-9025 is still In Progress, meaning remediation is not yet complete. If the engineer selects this issue, warn: "This issue is already in `In Progress`. It may be actively worked on." Wait for the engineer to choose whether to proceed or skip.
- **Stream scope:** rhtpa-2.1 maps to stream 2.1.x

#### TC-9026 -- CVE-2026-39330 (openssl - Buffer overflow in X.509 parsing [rhtpa-2.2])

- **Current status:** Modified
- **Labels:** ai-cve-triaged
- **Linked Tasks:** None with type "Depend"
- **Handling:** Excluded from Ready for QA. No linked remediation Tasks with type "Depend" exist, so there is no remediation work to verify. This issue may need investigation -- it was triaged and reached Modified status but has no associated remediation tasks. Possible explanations:
  - Remediation tasks were created but not linked with the "Depend" link type
  - The issue was closed as not affected and later reopened
  - Remediation was handled outside the standard workflow
- **Stream scope:** rhtpa-2.2 maps to stream 2.2.x
