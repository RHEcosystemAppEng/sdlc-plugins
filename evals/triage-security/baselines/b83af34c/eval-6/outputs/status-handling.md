# Status-Aware Handling Decisions

This document records the status-aware handling decision for each issue listed in the discovery mode results, per the triage-security skill's status-aware handling rules.

## Untriaged Issues

### TC-9001 — CVE-2026-40112 h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2]
- **Current status**: New
- **Handling**: Proceed with full triage (default path). New issues are eligible for the complete 8-step triage workflow.

### TC-9002 — CVE-2026-40297 serde_json - Stack overflow on deeply nested input [rhtpa-2.1]
- **Current status**: New
- **Handling**: Proceed with full triage (default path). New issues are eligible for the complete 8-step triage workflow.

### TC-9003 — CVE-2026-40455 tokio - Race condition in task cancellation [rhtpa-2.2]
- **Current status**: In Progress
- **Handling**: WARNING -- This issue is already in `In Progress`. It may be actively worked on. Before triaging, the engineer should choose:
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue

### TC-9004 — CVE-2026-40518 ring - Timing side-channel in RSA verification [rhtpa-2.2]
- **Current status**: New
- **Handling**: Proceed with full triage (default path). New issues are eligible for the complete 8-step triage workflow.

## Triaged but still New

### TC-9010 — CVE-2026-39874 quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2]
- **Current status**: New
- **Handling**: This issue carries the `ai-cve-triaged` label but remains in New status. It was previously triaged but never moved forward. The engineer should evaluate whether follow-up or re-triage is needed.

## Ready for QA Candidates

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]
- **Current status**: Modified
- **Handling**: All linked remediation Tasks are complete (TC-9021: Done, TC-9022: Closed). This issue is a candidate for transition to ON_QA.

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]
- **Current status**: In Progress
- **Handling**: Remediation still in progress. TC-9024 is Done, but TC-9025 is still In Progress. Not ready for QA transition.

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]
- **Current status**: Modified
- **Handling**: No linked Tasks with "Depend" link type found. There is no remediation to verify. Not eligible for Ready for QA.
