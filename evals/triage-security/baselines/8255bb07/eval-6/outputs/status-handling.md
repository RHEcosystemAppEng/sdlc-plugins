# Status-Aware Handling Decisions

Per the triage-security skill, each issue's current Jira status determines how it should be handled if selected for triage or action.

---

## Untriaged Issues (Query 1)

### TC-9001 — CVE-2026-40112 (h2 - HTTP/2 rapid reset vulnerability)
- **Status:** New
- **Handling:** Proceed with full triage (default path). No warnings required. Execute Steps 0.7 through 8 in sequence: assign, transition to Assigned, extract CVE data, analyze version impact, correct Affects Versions, check duplicates, check lifecycle, check already-fixed, and create remediation tasks if affected.

### TC-9002 — CVE-2026-40297 (serde_json - Stack overflow on deeply nested input)
- **Status:** New
- **Handling:** Proceed with full triage (default path). No warnings required. Same full triage workflow as TC-9001.

### TC-9003 — CVE-2026-40455 (tokio - Race condition in task cancellation)
- **Status:** In Progress
- **Handling:** Warn the user before proceeding.
  > "This issue is already in `In Progress`. It may be actively worked on."
  
  Present two options:
  1. **Proceed with triage anyway** — useful to verify version impact or update Affects Versions even on an in-progress issue.
  2. **Skip this issue** — return to the discovery list.
  
  Wait for user selection before taking any action.

### TC-9004 — CVE-2026-40518 (ring - Timing side-channel in RSA verification)
- **Status:** New
- **Handling:** Proceed with full triage (default path). No warnings required. Same full triage workflow as TC-9001.

---

## Triaged but still New (Query 2)

### TC-9010 — CVE-2026-39874 (quinn-proto - Panic on malformed QUIC frame)
- **Status:** New
- **Handling:** Proceed with full triage (default path). Although this issue carries the `ai-cve-triaged` label (indicating it was previously triaged), it remains in New status, which suggests remediation was never started. The New status means no active-work warning is needed. The engineer should be informed that this is a previously triaged issue that never progressed, and re-triage may be warranted to verify whether the original triage conclusions still hold or if circumstances have changed.

---

## Ready for QA Candidates (Query 3)

### TC-9020 — CVE-2026-38901 (hyper - HTTP request smuggling)
- **Status:** Modified
- **Handling:** This issue has all linked remediation tasks completed (TC-9021: Done, TC-9022: Closed). It is a candidate for ON_QA transition.
  
  If selected for action: suggest transitioning to ON_QA status. Present the recommendation:
  > "All remediation tasks for TC-9020 are complete (TC-9021 Done, TC-9022 Closed). Consider transitioning this issue to ON_QA."
  
  Wait for engineer confirmation before executing the transition.

### TC-9023 — CVE-2026-39102 (rustls - Certificate validation bypass)
- **Status:** In Progress
- **Handling:** Excluded from Ready for QA list. Remediation task TC-9025 is still In Progress, meaning remediation is not yet complete. This issue cannot be moved to ON_QA until all linked remediation tasks reach Done or Closed status.
  
  If selected for triage instead: warn the user that the issue is in `In Progress` status and may be actively worked on. Present the proceed/skip options as described in the status-aware handling rules.

### TC-9026 — CVE-2026-39330 (openssl - Buffer overflow in X.509 parsing)
- **Status:** Modified
- **Handling:** Excluded from Ready for QA list. No linked Tasks with link type "Depend" were found, so there is no completed remediation to verify. This issue may need investigation to determine why no remediation tasks exist — possible reasons include: the fix was applied without task tracking, the issue was resolved through a different mechanism, or remediation tasks were never created.
  
  If selected for triage: the Modified status suggests active work has occurred. Warn the user that the issue may be actively worked on before proceeding with any triage actions.

---

## Summary of Status-Handling Rules Applied

| Status | Rule | Issues |
|--------|------|--------|
| New | Proceed with full triage | TC-9001, TC-9002, TC-9004, TC-9010 |
| In Progress | Warn: may be actively worked on; ask to proceed or skip | TC-9003, TC-9023 |
| Modified | Context-dependent: check for QA readiness (Query 3) or warn if selected for triage | TC-9020, TC-9026 |
| Closed / Done / Resolved | Warn: already closed; ask to re-triage or skip | (none in current results) |
