# Status-Aware Handling Decisions

This document describes the status-aware handling decision for each issue discovered in the three JQL queries, following the triage-security skill's Discovery Mode rules.

---

## Untriaged Issues

### TC-9001 -- CVE-2026-40112 (h2 - HTTP/2 rapid reset vulnerability)
- **Status**: New
- **Handling**: Proceed with full triage (Steps 1-7). This is the default path for New issues -- no warnings or special handling required.
- **Stream scope**: rhtpa-2.2 (maps to stream 2.2.x)

### TC-9002 -- CVE-2026-40297 (serde_json - Stack overflow on deeply nested input)
- **Status**: New
- **Handling**: Proceed with full triage (Steps 1-7). This is the default path for New issues -- no warnings or special handling required.
- **Stream scope**: rhtpa-2.1 (maps to stream 2.1.x)

### TC-9003 -- CVE-2026-40455 (tokio - Race condition in task cancellation)
- **Status**: In Progress
- **Handling**: **WARNING** -- This issue is already in `In Progress`. It may be actively worked on. Before proceeding, the engineer must be asked:
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue
- **Stream scope**: rhtpa-2.2 (maps to stream 2.2.x)
- **Note**: If the engineer chooses to skip, return to the discovery list or end the session.

### TC-9004 -- CVE-2026-40518 (ring - Timing side-channel in RSA verification)
- **Status**: New
- **Handling**: Proceed with full triage (Steps 1-7). This is the default path for New issues -- no warnings or special handling required.
- **Stream scope**: rhtpa-2.2 (maps to stream 2.2.x)

---

## Triaged but still New

### TC-9010 -- CVE-2026-39874 (quinn-proto - Panic on malformed QUIC frame)
- **Status**: New
- **Handling**: This issue was previously triaged (has `ai-cve-triaged` label) but remains in New status. It has never been actioned despite triage being completed. This may indicate:
  - Remediation tasks were not created or not acted on
  - The triage outcome was inconclusive
  - The issue was deprioritized
- **Recommendation**: Flag for engineer review. May need follow-up or re-triage to determine why it stalled after initial triage.
- **Stream scope**: rhtpa-2.2 (maps to stream 2.2.x)
- **If selected for triage**: Since status is New, proceed with full triage (default path). The existing `ai-cve-triaged` label suggests prior triage occurred, so the engineer should review what was done previously before re-triaging.

---

## Ready for QA Candidates

### TC-9020 -- CVE-2026-38901 (hyper - HTTP request smuggling)
- **Status**: Modified
- **Linked Tasks**: TC-9021 (Done), TC-9022 (Closed)
- **Handling**: All linked remediation Tasks are completed. This issue is **Ready for QA**. Suggest transitioning to ON_QA.
- **Stream scope**: rhtpa-2.2 (maps to stream 2.2.x)

### TC-9023 -- CVE-2026-39102 (rustls - Certificate validation bypass)
- **Status**: In Progress
- **Linked Tasks**: TC-9024 (Done), TC-9025 (In Progress)
- **Handling**: **Excluded from Ready for QA**. Remediation task TC-9025 is still In Progress -- remediation is not yet complete. This issue should remain in its current status until all linked Tasks reach Done or Closed.
- **Stream scope**: rhtpa-2.1 (maps to stream 2.1.x)
- **Note**: If this issue were selected for triage, the In Progress status would trigger a warning: "This issue is already in `In Progress`. It may be actively worked on." The engineer would be asked whether to proceed or skip.

### TC-9026 -- CVE-2026-39330 (openssl - Buffer overflow in X.509 parsing)
- **Status**: Modified
- **Linked Tasks**: None (no Depend links)
- **Handling**: **Excluded from Ready for QA**. No linked remediation Tasks with "Depend" link type exist -- there is no remediation to verify. This issue may need investigation to determine whether remediation tasks were never created or were linked with a different link type.
- **Stream scope**: rhtpa-2.2 (maps to stream 2.2.x)
