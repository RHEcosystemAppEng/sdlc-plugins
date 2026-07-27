# Status-Aware Handling Decisions

This document applies the status-aware handling rules from the triage-security skill to each issue found in the discovery queries. The rules determine how each issue should be handled if the engineer selects it for triage.

## Status Handling Rules Reference

| Status | Handling |
|--------|----------|
| **New** | Proceed with full triage (default path) |
| **In Progress / Code Review / QA** | Warn: issue may be actively worked on. Ask whether to (1) proceed with triage anyway, or (2) skip |
| **Closed / Done / Resolved** | Warn: issue is already closed. Ask whether to (1) re-triage, or (2) skip |
| **Modified** | Issue has been triaged and modified; verify status before proceeding |

---

## Query 1: Untriaged Issues

### TC-9001 — CVE-2026-40112 h2 (New)

- **Status**: New
- **Handling**: Proceed with full triage (default path).
- **Rationale**: Issue is in New status with no `ai-cve-triaged` label. This is an untriaged vulnerability ready for the standard 8-step triage workflow. Assign to current user, transition to Assigned, and begin Step 1 (Data Extraction).

### TC-9002 — CVE-2026-40297 serde_json (New)

- **Status**: New
- **Handling**: Proceed with full triage (default path).
- **Rationale**: Issue is in New status with no `ai-cve-triaged` label. Standard untriaged vulnerability. Assign to current user, transition to Assigned, and begin Step 1 (Data Extraction).

### TC-9003 — CVE-2026-40455 tokio (In Progress)

- **Status**: In Progress
- **Handling**: Warn before proceeding.
- **Warning**: "This issue is already in `In Progress`. It may be actively worked on."
- **Options**:
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue
- **Rationale**: The In Progress status indicates another engineer may already be working on this issue. Proceeding without checking could result in duplicate remediation effort or conflicting triage conclusions. The engineer must explicitly choose to proceed or skip.

### TC-9004 — CVE-2026-40518 ring (New)

- **Status**: New
- **Handling**: Proceed with full triage (default path).
- **Rationale**: Issue is in New status with no `ai-cve-triaged` label. Standard untriaged vulnerability. Assign to current user, transition to Assigned, and begin Step 1 (Data Extraction).

---

## Query 2: Triaged but still New

### TC-9010 — CVE-2026-39874 quinn-proto (New)

- **Status**: New
- **Handling**: Proceed with full triage (default path), but flag as potentially stale.
- **Flag**: This issue carries the `ai-cve-triaged` label but remains in New status. It was previously triaged but never actioned. This may indicate:
  - The prior triage concluded no action was needed but forgot to close/transition the issue
  - Remediation tasks were created but the issue was not transitioned
  - The prior triage was incomplete or abandoned
- **Recommendation**: Review the issue's comment history for prior triage notes before re-triaging. If prior triage was complete and correct, transition the issue to the appropriate status. If prior triage was incomplete, proceed with a fresh triage pass.

---

## Query 3: Ready for QA Candidates

### TC-9020 — CVE-2026-38901 hyper (Modified)

- **Status**: Modified
- **Handling**: Ready for QA transition.
- **Evidence**: All linked remediation Tasks are completed:
  - TC-9021: Done
  - TC-9022: Closed
- **Recommendation**: Consider transitioning to ON_QA. All remediation work is complete and this CVE is a candidate for QA verification. The engineer should verify that the fixes in TC-9021 and TC-9022 adequately address the vulnerability before transitioning.

### TC-9023 — CVE-2026-39102 rustls (In Progress)

- **Status**: In Progress
- **Handling**: Not ready for QA; warn if selected for triage.
- **Warning**: "This issue is already in `In Progress`. It may be actively worked on."
- **Exclusion reason**: Remediation task TC-9025 is still In Progress. The issue cannot move to ON_QA until all remediation Tasks are completed.
- **Options if selected for triage**:
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue

### TC-9026 — CVE-2026-39330 openssl (Modified)

- **Status**: Modified
- **Handling**: Not ready for QA; may need investigation.
- **Exclusion reason**: No linked remediation Tasks with type "Depend" found. This issue has been triaged (carries `ai-cve-triaged` label) and modified, but has no associated remediation tasks to verify.
- **Recommendation**: Investigate why this triaged issue has no remediation tasks linked. Possible explanations:
  - The prior triage concluded no fix was needed (Case C) but did not close the issue
  - Remediation tasks were created but not linked with the "Depend" link type
  - The prior triage was incomplete
- **Action**: If selected, review the issue's comment history and linked issues for context before deciding on next steps.
