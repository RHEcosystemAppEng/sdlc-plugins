# Status-Aware Handling Decisions

Per the triage-security skill's status-aware handling rules, each issue's current
Jira status determines how triage should proceed:

- **New** -- proceed with full triage (default path)
- **In Progress / Code Review / QA** -- warn that the issue may be actively worked on; ask whether to proceed with triage or skip
- **Closed / Done / Resolved** -- warn that the issue is already closed; ask whether to re-triage or skip
- **Modified** -- non-terminal status; proceed with appropriate action (e.g., QA transition if ready)

---

## Query 1: Untriaged Issues

### TC-9001 — CVE-2026-40112 h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2]

- **Current status:** New
- **Handling decision:** Proceed with full triage (default path)
- **Rationale:** Issue is in New status with no `ai-cve-triaged` label. Standard untriaged issue ready for the complete 8-step triage workflow. Stream scope: 2.2.x.

### TC-9002 — CVE-2026-40297 serde_json - Stack overflow on deeply nested input [rhtpa-2.1]

- **Current status:** New
- **Handling decision:** Proceed with full triage (default path)
- **Rationale:** Issue is in New status with no `ai-cve-triaged` label. Standard untriaged issue ready for the complete 8-step triage workflow. Stream scope: 2.1.x.

### TC-9003 — CVE-2026-40455 tokio - Race condition in task cancellation [rhtpa-2.2]

- **Current status:** In Progress
- **Handling decision:** Warn user before proceeding
- **Warning:** "This issue is already in `In Progress`. It may be actively worked on."
- **Options presented to user:**
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue
- **Rationale:** The In Progress status indicates someone may already be working on this issue. The engineer must confirm whether to proceed or skip. If the user chooses to skip, return to the discovery list. Stream scope: 2.2.x.

### TC-9004 — CVE-2026-40518 ring - Timing side-channel in RSA verification [rhtpa-2.2]

- **Current status:** New
- **Handling decision:** Proceed with full triage (default path)
- **Rationale:** Issue is in New status with no `ai-cve-triaged` label. Standard untriaged issue ready for the complete 8-step triage workflow. Stream scope: 2.2.x.

---

## Query 2: Triaged but still New (stale issues)

### TC-9010 — CVE-2026-39874 quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2]

- **Current status:** New
- **Labels include:** ai-cve-triaged
- **Handling decision:** Proceed with full triage (default path), but flagged as stale
- **Rationale:** Despite carrying the `ai-cve-triaged` label, this issue remains in New status, meaning it was triaged previously but never actioned (no remediation tasks were created, or they were created but the issue was never transitioned). This may need follow-up or re-triage to determine why triage did not result in forward progress. On selection, full triage proceeds since the status is New. Stream scope: 2.2.x.

---

## Query 3: Ready for QA Candidates

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Current status:** Modified
- **Labels include:** ai-cve-triaged
- **Linked remediation tasks:** TC-9021 (Done), TC-9022 (Closed)
- **Handling decision:** Ready for QA transition
- **Recommended action:** Transition to ON_QA. All linked remediation tasks with link type "Depend" are complete (Done or Closed). The CVE remediation is fully implemented and ready for quality assurance verification.
- **Rationale:** Modified is a non-terminal status indicating work has been completed. All remediation tasks are in terminal states, confirming the fix is fully landed. Stream scope: 2.2.x.

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Current status:** In Progress
- **Labels include:** ai-cve-triaged
- **Linked remediation tasks:** TC-9024 (Done), TC-9025 (In Progress)
- **Handling decision:** Excluded from Ready for QA; warn if selected for triage
- **Warning (if selected):** "This issue is already in `In Progress`. It may be actively worked on."
- **Options presented to user (if selected):**
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue
- **Rationale:** TC-9025 is still In Progress, so remediation is incomplete. This issue cannot transition to ON_QA until all linked remediation tasks reach Done or Closed. Additionally, the In Progress status triggers the active-work warning if an engineer selects it for triage. Stream scope: 2.1.x.

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Current status:** Modified
- **Labels include:** ai-cve-triaged
- **Linked remediation tasks:** None (no "Depend" links)
- **Handling decision:** Excluded from Ready for QA
- **Rationale:** No linked Tasks with link type "Depend" exist on this issue. Without remediation tasks to verify, there is no evidence that a fix has been implemented. This issue may need investigation to determine why no remediation tasks were created — it could indicate the triage concluded with a close recommendation that was not executed, or that remediation tasks were created without proper linkage. If selected for triage, it would proceed normally since Modified is a non-terminal, non-warning status. Stream scope: 2.2.x.

---

## Summary of Handling Decisions

| Issue | Status | Decision | Action |
|-------|--------|----------|--------|
| TC-9001 | New | Proceed | Full triage |
| TC-9002 | New | Proceed | Full triage |
| TC-9003 | In Progress | Warn | Ask user: proceed or skip |
| TC-9004 | New | Proceed | Full triage |
| TC-9010 | New (stale) | Proceed | Full triage (flagged as stale) |
| TC-9020 | Modified | Ready for QA | Transition to ON_QA |
| TC-9023 | In Progress | Excluded / Warn | Remediation incomplete; warn if selected |
| TC-9026 | Modified | Excluded | No remediation tasks linked |
