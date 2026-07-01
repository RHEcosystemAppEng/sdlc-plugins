# Status-Aware Handling Decisions

This document details the status-aware handling applied to each issue discovered in the three JQL queries. Per the triage-security skill, the current Jira status of each issue determines how it should be handled when selected for triage.

---

## Query 1: Untriaged Issues

### TC-9001 — Status: New

- **Handling**: Proceed with full triage (default path)
- **Rationale**: Issue is in `New` status with no `ai-cve-triaged` label. This is the standard entry point for triage. No warnings or special handling required.
- **CVE**: CVE-2026-40112 (h2 - HTTP/2 rapid reset vulnerability)
- **Stream**: rhtpa-2.2

### TC-9002 — Status: New

- **Handling**: Proceed with full triage (default path)
- **Rationale**: Issue is in `New` status with no `ai-cve-triaged` label. Standard triage path applies.
- **CVE**: CVE-2026-40297 (serde_json - Stack overflow on deeply nested input)
- **Stream**: rhtpa-2.1

### TC-9003 — Status: In Progress

- **Handling**: Warning -- active work detected
- **Warning presented to engineer**:

  > "This issue is already in `In Progress`. It may be actively worked on."
  >
  > Options:
  > 1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  > 2. Skip this issue

- **Rationale**: The `In Progress` status indicates another engineer may already be working on this issue. Proceeding without acknowledgment risks creating duplicate remediation tasks or conflicting Affects Versions changes. The engineer must explicitly choose before triage continues.
- **CVE**: CVE-2026-40455 (tokio - Race condition in task cancellation)
- **Stream**: rhtpa-2.2

### TC-9004 — Status: New

- **Handling**: Proceed with full triage (default path)
- **Rationale**: Issue is in `New` status with no `ai-cve-triaged` label. Standard triage path applies.
- **CVE**: CVE-2026-40518 (ring - Timing side-channel in RSA verification)
- **Stream**: rhtpa-2.2

---

## Query 2: Triaged but still New

### TC-9010 — Status: New (with ai-cve-triaged label)

- **Handling**: Proceed with full triage (default path for New status)
- **Rationale**: Although this issue carries the `ai-cve-triaged` label (indicating a prior triage pass), it remains in `New` status. This is a stale issue -- it was triaged but never moved forward. The engineer should investigate why:
  - Were remediation tasks created but the issue never transitioned?
  - Was the prior triage incomplete or declined by the engineer?
  - Does it need re-triage with updated data?
- **Follow-up suggested**: Check for existing remediation tasks linked to this issue before running a full re-triage. A re-triage may update the version impact table or create new remediation tasks if the prior triage was outdated.
- **CVE**: CVE-2026-39874 (quinn-proto - Panic on malformed QUIC frame)
- **Stream**: rhtpa-2.2

---

## Query 3: Ready for QA Candidates

### TC-9020 — Status: Modified

- **Handling**: Ready for QA transition
- **Rationale**: All linked remediation Tasks are completed:
  - TC-9021: Status = Done
  - TC-9022: Status = Closed
  
  Both tasks were linked via "Depend" link type, confirming they are remediation tasks created by triage. Since all remediation is complete, this CVE is a candidate for ON_QA transition.
- **Suggested action**: Transition TC-9020 to ON_QA. All linked remediation tasks have been completed.
- **CVE**: CVE-2026-38901 (hyper - HTTP request smuggling)
- **Stream**: rhtpa-2.2

### TC-9023 — Status: In Progress

- **Handling**: Excluded from Ready for QA -- remediation incomplete
- **Rationale**: Linked remediation Tasks show mixed completion:
  - TC-9024: Status = Done (complete)
  - TC-9025: Status = In Progress (still open)
  
  Because TC-9025 is still `In Progress`, remediation is not complete. This issue cannot be transitioned to ON_QA until all linked remediation tasks reach Done or Closed status.
- **CVE**: CVE-2026-39102 (rustls - Certificate validation bypass)
- **Stream**: rhtpa-2.1

### TC-9026 — Status: Modified

- **Handling**: Excluded from Ready for QA -- no remediation tasks linked
- **Rationale**: No linked Tasks with link type "Depend" exist on this issue. Without remediation tasks, there is no remediation to verify as complete. This could indicate:
  - The triage closed the issue (Case C: not affected) but the issue was later re-opened
  - Remediation tasks were created but never linked
  - The triage was incomplete
  
  This issue should not be transitioned to ON_QA because there are no completed remediation tasks to verify.
- **CVE**: CVE-2026-39330 (openssl - Buffer overflow in X.509 parsing)
- **Stream**: rhtpa-2.2

---

## Decision Matrix Summary

| Issue | Status | ai-cve-triaged? | Handling Decision | Action |
|-------|--------|-----------------|-------------------|--------|
| TC-9001 | New | No | Full triage | Proceed |
| TC-9002 | New | No | Full triage | Proceed |
| TC-9003 | In Progress | No | Warning: active work | Ask engineer to proceed or skip |
| TC-9004 | New | No | Full triage | Proceed |
| TC-9010 | New | Yes | Stale triage -- re-examine | Investigate prior triage, then proceed |
| TC-9020 | Modified | Yes | Ready for QA | Suggest transition to ON_QA |
| TC-9023 | In Progress | Yes | Not Ready for QA | Wait for TC-9025 to complete |
| TC-9026 | Modified | Yes | Not Ready for QA | No remediation tasks to verify |
