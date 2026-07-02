# Status-Aware Handling Decisions

Per the triage-security skill, when the user selects an issue from the discovery
listing, its current Jira status determines how triage proceeds. Below is the
status-aware handling decision for each listed issue.

---

## Untriaged Issues (Query 1)

### TC-9001 -- CVE-2026-40112 (h2 - HTTP/2 rapid reset vulnerability)
- **Current status:** New
- **Handling:** Proceed with full triage (default path). No warnings required.
- **Action:** Execute Steps 0.7 through 8 in sequence. Assign issue, transition to Assigned, extract CVE data, perform version impact analysis, and continue through remediation.

### TC-9002 -- CVE-2026-40297 (serde_json - Stack overflow on deeply nested input)
- **Current status:** New
- **Handling:** Proceed with full triage (default path). No warnings required.
- **Action:** Execute Steps 0.7 through 8 in sequence. Assign issue, transition to Assigned, extract CVE data, perform version impact analysis, and continue through remediation.

### TC-9003 -- CVE-2026-40455 (tokio - Race condition in task cancellation)
- **Current status:** In Progress
- **Handling:** Warn the user before proceeding.
- **Warning:** "This issue is already in `In Progress`. It may be actively worked on."
- **Options presented to user:**
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue
- **If user chooses to skip:** Return to the discovery list or end the session.
- **If user chooses to proceed:** Execute Steps 0.7 through 8, but skip the transition to Assigned in Step 0.7 since the issue is already past New status. Assignment (Step 0.7, sub-step 2) still proceeds to record the current user.

### TC-9004 -- CVE-2026-40518 (ring - Timing side-channel in RSA verification)
- **Current status:** New
- **Handling:** Proceed with full triage (default path). No warnings required.
- **Action:** Execute Steps 0.7 through 8 in sequence. Assign issue, transition to Assigned, extract CVE data, perform version impact analysis, and continue through remediation.

---

## Triaged but still New (Query 2)

### TC-9010 -- CVE-2026-39874 (quinn-proto - Panic on malformed QUIC frame)
- **Current status:** New
- **Handling:** Proceed with full triage (default path). No warnings required.
- **Note:** This issue has the `ai-cve-triaged` label, indicating it was previously triaged but remains in New status. It may need follow-up or re-triage. Since the status is New, standard triage proceeds without warnings. The label will be re-applied at the end of triage (it is already present, so no change needed).
- **Action:** Execute Steps 0.7 through 8 in sequence. This is effectively a re-triage to determine why the issue was not actioned after the initial triage.

---

## Ready for QA (Query 3)

### TC-9020 -- CVE-2026-38901 (hyper - HTTP request smuggling)
- **Current status:** Modified
- **Handling:** This issue appears in the Ready for QA list because all linked remediation tasks are complete (TC-9021: Done, TC-9022: Closed). The recommended action is to transition to ON_QA rather than to perform a full triage.
- **If the user selects this for triage instead:** Since Modified is not New, and is not Closed/Done/Resolved, it falls into the active-work category. Warn the user: "This issue is already in `Modified`. It may be actively worked on." Present the option to proceed with triage (e.g., to verify version impact) or skip.
- **Recommended action:** Transition TC-9020 to ON_QA since all remediation work is complete.

### TC-9023 -- CVE-2026-39102 (rustls - Certificate validation bypass)
- **Current status:** In Progress
- **Handling:** Warn the user before proceeding.
- **Warning:** "This issue is already in `In Progress`. It may be actively worked on."
- **Context:** This issue was excluded from the Ready for QA list because TC-9025 is still In Progress. Remediation is not yet complete.
- **Options presented to user:**
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue
- **If user chooses to skip:** Return to the discovery list or end the session.
- **If user chooses to proceed:** Execute Steps 0.7 through 8, skipping the Assigned transition since the issue is already past New status.

### TC-9026 -- CVE-2026-39330 (openssl - Buffer overflow in X.509 parsing)
- **Current status:** Modified
- **Handling:** This issue was excluded from the Ready for QA list because it has no linked Tasks with link type "Depend" -- there is no remediation work to verify.
- **If the user selects this for triage:** Since Modified is not New, and is not Closed/Done/Resolved, warn the user: "This issue is already in `Modified`. It may be actively worked on." Present the option to proceed with triage (e.g., to verify version impact or check why no remediation tasks exist) or skip.
- **Recommended investigation:** Determine why this triaged issue in Modified status has no linked remediation tasks. It may need remediation tasks created, or it may have been resolved through other means.

---

## Summary of Status-Handling Rules Applied

| Status | Rule | Issues |
|--------|------|--------|
| New | Proceed with full triage (default path) | TC-9001, TC-9002, TC-9004, TC-9010 |
| In Progress | Warn: may be actively worked on. Ask to proceed or skip. | TC-9003, TC-9023 |
| Modified | Warn: may be actively worked on. Ask to proceed or skip. For Ready for QA candidates, suggest ON_QA transition instead. | TC-9020, TC-9026 |
| Closed / Done / Resolved | Warn: already closed. Ask to re-triage or skip. | (none in current results) |
