# Status-Aware Handling Decisions

Per the triage-security skill's status-aware handling rules, each discovered issue is assessed based on its current Jira status to determine the appropriate triage action.

---

## Untriaged Issues

### TC-9001 -- CVE-2026-40112 h2 (New)

- **Status:** New
- **Handling:** Proceed with full triage (default path). This issue is in its initial state and ready for the complete 8-step version-aware triage workflow.

### TC-9002 -- CVE-2026-40297 serde_json (New)

- **Status:** New
- **Handling:** Proceed with full triage (default path). This issue is in its initial state and ready for the complete 8-step version-aware triage workflow.

### TC-9003 -- CVE-2026-40455 tokio (In Progress)

- **Status:** In Progress
- **Handling:** Warn the user: "This issue is already in `In Progress`. It may be actively worked on." Ask whether to:
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue

### TC-9004 -- CVE-2026-40518 ring (New)

- **Status:** New
- **Handling:** Proceed with full triage (default path). This issue is in its initial state and ready for the complete 8-step version-aware triage workflow.

---

## Triaged but still New

### TC-9010 -- CVE-2026-39874 quinn-proto (New)

- **Status:** New (with `ai-cve-triaged` label)
- **Handling:** This issue was previously triaged but never moved past New status. It may need follow-up or re-triage. Since the status is New, standard triage flow applies if the engineer selects it for re-triage. Flagged for the engineer's attention as a potentially stale triaged issue that was never actioned.

---

## Ready for QA Candidates

### TC-9020 -- CVE-2026-38901 hyper (Modified)

- **Status:** Modified
- **Handling:** Ready for QA. All linked remediation Tasks are completed:
  - TC-9021: Done
  - TC-9022: Closed
- **Recommendation:** Consider transitioning to ON_QA. The Modified status indicates triage and remediation are complete, and all dependent work has finished.

### TC-9023 -- CVE-2026-39102 rustls (In Progress)

- **Status:** In Progress
- **Handling:** NOT ready for QA. Remediation is still in progress:
  - TC-9024: Done
  - TC-9025: In Progress (still open)
- **Reason for exclusion:** At least one linked remediation Task (TC-9025) is still open. This issue cannot be transitioned to ON_QA until all remediation work is complete.
- **Status-aware note:** Since this issue is In Progress, if the engineer selects it for triage, they should be warned: "This issue is already in `In Progress`. It may be actively worked on."

### TC-9026 -- CVE-2026-39330 openssl (Modified)

- **Status:** Modified
- **Handling:** NOT ready for QA. No linked Tasks with Depend link type exist.
- **Reason for exclusion:** No remediation Tasks are linked to this issue. Without remediation work to verify, this issue cannot be considered for ON_QA transition. The issue may need investigation to determine if remediation tasks were never created, were linked with a different link type, or if the issue was resolved through other means.
