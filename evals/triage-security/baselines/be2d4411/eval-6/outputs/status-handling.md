# Status-Aware Handling Decisions

Per the triage-security skill's status-aware handling rules, each discovered issue is evaluated based on its current Jira status. The handling determines whether the issue proceeds to full triage, triggers a warning, or requires confirmation before proceeding.

---

## Untriaged Issues (Query 1)

### TC-9001 — CVE-2026-40112 (h2 - HTTP/2 rapid reset vulnerability)
- **Status:** New
- **Handling:** Proceed with full triage (default path). No warnings required. This issue is in the expected initial state for a freshly created PSIRT Vulnerability.

### TC-9002 — CVE-2026-40297 (serde_json - Stack overflow on deeply nested input)
- **Status:** New
- **Handling:** Proceed with full triage (default path). No warnings required.

### TC-9003 — CVE-2026-40455 (tokio - Race condition in task cancellation)
- **Status:** In Progress
- **Handling:** **Warning required.** This issue is already in "In Progress" status. It may be actively worked on by another engineer. Present the following warning before proceeding:

  > "This issue is already in In Progress. It may be actively worked on."

  Ask the engineer whether to:
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue

  If the engineer chooses to skip, return to the discovery list or end the session.

### TC-9004 — CVE-2026-40518 (ring - Timing side-channel in RSA verification)
- **Status:** New
- **Handling:** Proceed with full triage (default path). No warnings required.

---

## Triaged but still New (Query 2)

### TC-9010 — CVE-2026-39874 (quinn-proto - Panic on malformed QUIC frame)
- **Status:** New
- **Handling:** This issue was previously triaged (carries the `ai-cve-triaged` label) but remains in New status. It may need follow-up or re-triage. Since the status is New, full triage can proceed without warnings if the engineer selects it for re-triage. The stale status suggests prior triage actions may not have been fully actioned (e.g., remediation tasks were created but the issue was never transitioned).

---

## Ready for QA Candidates (Query 3)

### TC-9020 — CVE-2026-38901 (hyper - HTTP request smuggling)
- **Status:** Modified
- **Handling:** All linked remediation Tasks are completed (TC-9021: Done, TC-9022: Closed). This issue qualifies for transition to ON_QA. Recommend: "Consider transitioning TC-9020 to ON_QA." No full triage needed -- the issue has already been triaged and remediated.

### TC-9023 — CVE-2026-39102 (rustls - Certificate validation bypass)
- **Status:** In Progress
- **Handling:** Excluded from Ready for QA. Linked remediation Task TC-9025 is still In Progress, so remediation is not yet complete. If the engineer selects this issue for triage, the In Progress status triggers a warning:

  > "This issue is already in In Progress. It may be actively worked on."

  Ask whether to proceed with triage or skip.

### TC-9026 — CVE-2026-39330 (openssl - Buffer overflow in X.509 parsing)
- **Status:** Modified
- **Handling:** Excluded from Ready for QA. No linked Tasks with type "Depend" exist, so there is no remediation to verify. This issue may need investigation -- a triaged CVE in Modified status without remediation tasks is unusual and may indicate the tasks were not created or were unlinked. If the engineer selects this issue, triage can proceed (Modified is not a terminal status), but the absence of remediation tasks should be flagged.

---

## Summary

| Issue | Status | Handling Decision |
|-------|--------|-------------------|
| TC-9001 | New | Full triage -- no warnings |
| TC-9002 | New | Full triage -- no warnings |
| TC-9003 | In Progress | Warning: may be actively worked on; ask to proceed or skip |
| TC-9004 | New | Full triage -- no warnings |
| TC-9010 | New (stale) | Re-triage eligible -- previously triaged but never actioned |
| TC-9020 | Modified | Ready for QA -- all remediation Tasks completed; suggest ON_QA transition |
| TC-9023 | In Progress | Excluded from QA -- TC-9025 still In Progress; warning if selected |
| TC-9026 | Modified | Excluded from QA -- no Depend links; flag absence of remediation tasks |
