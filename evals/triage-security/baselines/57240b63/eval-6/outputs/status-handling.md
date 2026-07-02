# Status-Aware Handling Decisions

Per the triage-security skill's status-aware handling rules, each discovered issue receives a handling decision based on its current Jira status.

## Handling Rules Reference

| Status | Action |
|--------|--------|
| **New** | Proceed with full triage (default path) |
| **In Progress / Code Review / QA** | Warn: "This issue is already in `<status>`. It may be actively worked on." Ask whether to (1) proceed with triage anyway, or (2) skip this issue. |
| **Closed / Done / Resolved** | Warn: "This issue is already closed." Ask whether to (1) re-triage, or (2) skip this issue. |

---

## Untriaged Issues

### TC-9001 — CVE-2026-40112 h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2]
- **Status:** New
- **Handling:** Proceed with full triage (default path). No warnings required.

### TC-9002 — CVE-2026-40297 serde_json - Stack overflow on deeply nested input [rhtpa-2.1]
- **Status:** New
- **Handling:** Proceed with full triage (default path). No warnings required.

### TC-9003 — CVE-2026-40455 tokio - Race condition in task cancellation [rhtpa-2.2]
- **Status:** In Progress
- **Handling:** Warn the user: "This issue is already in `In Progress`. It may be actively worked on." Ask whether to:
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue

### TC-9004 — CVE-2026-40518 ring - Timing side-channel in RSA verification [rhtpa-2.2]
- **Status:** New
- **Handling:** Proceed with full triage (default path). No warnings required.

---

## Triaged but still New

### TC-9010 — CVE-2026-39874 quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2]
- **Status:** New
- **Handling:** Proceed with full triage (default path). No warnings required. However, this issue is flagged as stale: it was previously triaged (`ai-cve-triaged` label present) but remains in New status. This suggests the triage outcome was never actioned — it may need follow-up or re-triage to verify the prior analysis is still current.

---

## Ready for QA Candidates

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]
- **Status:** Modified
- **Linked remediation tasks:** TC-9021 (Done), TC-9022 (Closed)
- **Handling:** All linked remediation Tasks with Depend links are completed (Done or Closed). This issue is a candidate for ON_QA transition. If the user selects this issue, the In Progress/Code Review/QA status-aware warning does not apply since Modified is a distinct workflow state indicating remediation is complete. Recommend: "Consider transitioning to ON_QA."

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]
- **Status:** In Progress
- **Linked remediation tasks:** TC-9024 (Done), TC-9025 (In Progress)
- **Handling:** Excluded from Ready for QA list because TC-9025 is still In Progress — remediation is not yet complete. If the user selects this issue for triage, warn: "This issue is already in `In Progress`. It may be actively worked on." Ask whether to proceed or skip.

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]
- **Status:** Modified
- **Linked remediation tasks:** None (no Depend links)
- **Handling:** Excluded from Ready for QA list because no linked Tasks with type "Depend" exist — there is no remediation to verify. If the user selects this issue, it may need investigation as to why no remediation tasks were created despite being in Modified status.
