# Status-Aware Handling Decisions

This document records the status-aware handling decision for each issue surfaced in
discovery mode, following the triage-security skill's status-aware handling protocol.

## Handling Protocol Reference

| Current Status | Handling |
|----------------|----------|
| **New** | Proceed with full triage (default path) |
| **In Progress / Code Review / QA** | Warn: issue may be actively worked on. Offer: (1) Proceed with triage anyway, (2) Skip |
| **Closed / Done / Resolved** | Warn: issue is already closed. Offer: (1) Re-triage to verify fix coverage, (2) Skip |
| **Modified** | Issue has been modified post-triage; evaluate context before proceeding |

---

## Untriaged Issues (Query 1)

### TC-9001 -- CVE-2026-40112 h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2]

- **Status**: New
- **Decision**: Proceed with full triage (default path)
- **Rationale**: Issue is in New status and has not been triaged (no `ai-cve-triaged` label). Standard untriaged issue -- execute Steps 0 through 8 in sequence. Stream scope: 2.2.x (from summary suffix `[rhtpa-2.2]`).

### TC-9002 -- CVE-2026-40297 serde_json - Stack overflow on deeply nested input [rhtpa-2.1]

- **Status**: New
- **Decision**: Proceed with full triage (default path)
- **Rationale**: Issue is in New status and has not been triaged. Standard untriaged issue -- execute full triage. Stream scope: 2.1.x (from summary suffix `[rhtpa-2.1]`).

### TC-9003 -- CVE-2026-40455 tokio - Race condition in task cancellation [rhtpa-2.2]

- **Status**: In Progress
- **Decision**: Warn engineer before proceeding
- **Rationale**: This issue is already in In Progress status, which indicates it may be actively worked on by another engineer. The skill must present a warning:

  > "This issue is already in `In Progress`. It may be actively worked on."
  >
  > Options:
  > 1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  > 2. Skip this issue

  The engineer must choose before triage can proceed. If they choose to proceed, execute Steps 0 through 8 but skip the Step 0.8 status transition (issue is already past New/Assigned). If they choose to skip, return to the discovery list.

### TC-9004 -- CVE-2026-40518 ring - Timing side-channel in RSA verification [rhtpa-2.2]

- **Status**: New
- **Decision**: Proceed with full triage (default path)
- **Rationale**: Issue is in New status and has not been triaged. Standard untriaged issue -- execute full triage. Stream scope: 2.2.x (from summary suffix `[rhtpa-2.2]`).

---

## Triaged but still New (Query 2)

### TC-9010 -- CVE-2026-39874 quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2]

- **Status**: New
- **Decision**: Flag for follow-up or re-triage
- **Rationale**: This issue carries the `ai-cve-triaged` label but remains in New status. This is anomalous -- a triaged issue should have been transitioned to Assigned or further. Possible explanations:
  - The previous triage did not result in remediation tasks (e.g., closed as not affected but the status transition failed)
  - The previous triage was interrupted before completing Step 0.8 (assign/transition)
  - The remediation outcome needs review

  The engineer should inspect the issue's comment history and decide whether to re-triage (which would re-run version impact analysis with current matrix data) or manually advance the issue status.

---

## Ready for QA Candidates (Query 3)

### TC-9020 -- CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status**: Modified
- **Decision**: Ready for ON_QA transition
- **Rationale**: All linked remediation Tasks with Depend link type are in terminal status:
  - TC-9021 (Task) -- Done
  - TC-9022 (Task) -- Closed

  All remediation work is complete. This issue is a candidate for transitioning to ON_QA status. The engineer should verify that the fixes have been properly propagated to the release before transitioning.

### TC-9023 -- CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status**: In Progress
- **Decision**: Not ready for QA -- remediation still in progress
- **Rationale**: Linked remediation Tasks show mixed completion:
  - TC-9024 (Task) -- Done
  - TC-9025 (Task) -- In Progress (still active)

  TC-9025 must reach Done or Closed before this issue can be considered for ON_QA. No action needed at this time -- the issue will appear in subsequent discovery runs until all remediation is complete.

### TC-9026 -- CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status**: Modified
- **Decision**: Not ready for QA -- no remediation tasks linked
- **Rationale**: This issue has no linked Tasks with the Depend link type. Without linked remediation tasks, there is no remediation work to verify as complete. Possible explanations:
  - Remediation tasks were created but not linked with the correct link type
  - The issue was triaged as not affected but not closed (status should be Closed if so)
  - The remediation approach does not use standard task linking

  The engineer should investigate whether remediation tasks exist and need linking, or whether this issue requires re-triage to create proper remediation tasks.
