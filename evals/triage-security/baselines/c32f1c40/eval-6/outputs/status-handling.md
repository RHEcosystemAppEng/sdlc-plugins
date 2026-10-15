# Status-Aware Handling Decisions

This document details the status-aware handling decision for each issue found in the discovery mode queries.

## Query 1: Untriaged Issues

### TC-9001 — CVE-2026-40112 (New)

- **Status**: New
- **Handling**: **Proceed with full triage** (default path). This issue is in New status and has not been triaged (no `ai-cve-triaged` label). Ready for standard triage workflow starting from Step 0.8 (Assign and Transition).
- **CVE**: CVE-2026-40112 — h2 HTTP/2 rapid reset vulnerability
- **Stream**: rhtpa-2.2 (scoped)

### TC-9002 — CVE-2026-40297 (New)

- **Status**: New
- **Handling**: **Proceed with full triage** (default path). This issue is in New status and has not been triaged. Ready for standard triage workflow.
- **CVE**: CVE-2026-40297 — serde_json stack overflow on deeply nested input
- **Stream**: rhtpa-2.1 (scoped)

### TC-9004 — CVE-2026-40518 (New)

- **Status**: New
- **Handling**: **Proceed with full triage** (default path). This issue is in New status and has not been triaged. Ready for standard triage workflow.
- **CVE**: CVE-2026-40518 — ring timing side-channel in RSA verification
- **Stream**: rhtpa-2.2 (scoped)

### TC-9003 — CVE-2026-40455 (In Progress)

- **Status**: In Progress
- **Handling**: **Warning — active work detected.**

  > This issue is already in `In Progress`. It may be actively worked on.

  Options presented to the engineer:
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue

  The In Progress status indicates another engineer may already be triaging or remediating this issue. Proceeding without coordination risks duplicate effort or conflicting mutations.

- **CVE**: CVE-2026-40455 — tokio race condition in task cancellation
- **Stream**: rhtpa-2.2 (scoped)

## Query 2: Triaged but still New

### TC-9010 — CVE-2026-39874 (New, triaged)

- **Status**: New
- **Handling**: This issue has the `ai-cve-triaged` label but remains in New status. It was triaged previously but never moved forward. This may indicate:
  - The triage completed but no remediation was needed (Case C close was not executed)
  - The engineer declined to execute the proposed Jira mutations
  - The triage was interrupted before completion

  **Recommendation**: Review the issue's comment history to determine why it remained in New status after triage. Consider re-triaging to verify the prior analysis and complete any pending actions.

- **CVE**: CVE-2026-39874 — quinn-proto panic on malformed QUIC frame
- **Stream**: rhtpa-2.2 (scoped)

## Query 3: Ready for QA Candidates

### TC-9020 — CVE-2026-38901 (Modified) — READY FOR QA

- **Status**: Modified
- **Handling**: All linked remediation Tasks are completed:
  - TC-9021: Done
  - TC-9022: Closed
- **Decision**: **Ready for QA.** Consider transitioning to ON_QA. All remediation work is complete and this CVE is a candidate for QA verification.
- **CVE**: CVE-2026-38901 — hyper HTTP request smuggling
- **Stream**: rhtpa-2.2 (scoped)

### TC-9023 — CVE-2026-39102 (In Progress) — NOT READY

- **Status**: In Progress
- **Handling**: Remediation is still in progress:
  - TC-9024: Done
  - TC-9025: **In Progress** (blocking)
- **Decision**: **Excluded from Ready for QA.** Cannot transition to ON_QA until TC-9025 completes. Remediation task TC-9025 is still being worked on.
- **CVE**: CVE-2026-39102 — rustls certificate validation bypass
- **Stream**: rhtpa-2.1 (scoped)

### TC-9026 — CVE-2026-39330 (Modified) — NOT READY

- **Status**: Modified
- **Handling**: No linked Tasks with type "Depend" exist.
- **Decision**: **Excluded from Ready for QA.** No remediation tasks are linked to this issue via "Depend" links. Without linked remediation tasks, there is nothing to verify for QA. This issue may need investigation to determine why no remediation was created -- it might have been closed and reopened, or remediation tasks were created without proper linkage.
- **CVE**: CVE-2026-39330 — openssl buffer overflow in X.509 parsing
- **Stream**: rhtpa-2.2 (scoped)

## Summary

| Issue | Status | Triaged? | Handling Decision |
|-------|--------|----------|-------------------|
| TC-9001 | New | No | Full triage |
| TC-9002 | New | No | Full triage |
| TC-9004 | New | No | Full triage |
| TC-9003 | In Progress | No | Warning: active work, ask engineer to proceed or skip |
| TC-9010 | New | Yes | Flagged as stale — triaged but never actioned |
| TC-9020 | Modified | Yes | Ready for QA — suggest ON_QA transition |
| TC-9023 | In Progress | Yes | Not ready — TC-9025 still In Progress |
| TC-9026 | Modified | Yes | Not ready — no Depend links |
