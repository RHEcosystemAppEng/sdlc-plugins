# Status-Aware Handling Decisions

Each issue from the discovery listing is evaluated against the status-aware handling
rules defined in the triage-security skill (SKILL.md, Inputs section).

---

## Untriaged Issues (Query 1)

### TC-9001 -- CVE-2026-40112 h2 [rhtpa-2.2]

- **Current status:** New
- **Handling:** Proceed with full triage (default path). No warnings required.
- **Next step:** Begin Step 0.7 (Assign and Transition to Assigned), then proceed through Steps 1-8.

### TC-9002 -- CVE-2026-40297 serde_json [rhtpa-2.1]

- **Current status:** New
- **Handling:** Proceed with full triage (default path). No warnings required.
- **Next step:** Begin Step 0.7 (Assign and Transition to Assigned), then proceed through Steps 1-8.

### TC-9003 -- CVE-2026-40455 tokio [rhtpa-2.2]

- **Current status:** In Progress
- **Handling:** Warn the user before proceeding.

  > "This issue is already in `In Progress`. It may be actively worked on."

  Options presented to the engineer:
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue

  If the user chooses to skip, return to the discovery list or end the session.

### TC-9004 -- CVE-2026-40518 ring [rhtpa-2.2]

- **Current status:** New
- **Handling:** Proceed with full triage (default path). No warnings required.
- **Next step:** Begin Step 0.7 (Assign and Transition to Assigned), then proceed through Steps 1-8.

---

## Triaged but still New (Query 2)

### TC-9010 -- CVE-2026-39874 quinn-proto [rhtpa-2.2]

- **Current status:** New
- **Labels:** ai-cve-triaged (already triaged)
- **Handling:** Proceed with full triage (default path for New status). No status warning required.
- **Note:** This issue was previously triaged (has `ai-cve-triaged` label) but remains in New status, indicating it was never actioned after triage. The engineer should consider whether it needs re-triage or follow-up to understand why it stalled.
- **Next step:** If selected, begin Step 0.7 (Assign and Transition to Assigned), then proceed through Steps 1-8 as a re-triage.

---

## Ready for QA Candidates (Query 3)

### TC-9020 -- CVE-2026-38901 hyper [rhtpa-2.2]

- **Current status:** Modified
- **Remediation tasks:** TC-9021 (Done), TC-9022 (Closed)
- **Handling:** All linked remediation tasks are complete. This issue is Ready for QA.
- **Recommendation:** Consider transitioning TC-9020 to ON_QA.
- **Status note:** Modified is not a warning-triggering status for triage purposes. If selected for individual triage, proceed normally.

### TC-9023 -- CVE-2026-39102 rustls [rhtpa-2.1]

- **Current status:** In Progress
- **Remediation tasks:** TC-9024 (Done), TC-9025 (In Progress)
- **Handling:** Excluded from Ready for QA -- TC-9025 is still In Progress. Remediation is not yet complete.
- **Status note:** If selected for individual triage, the In Progress status would trigger a warning:

  > "This issue is already in `In Progress`. It may be actively worked on."

  Options: 1) Proceed with triage anyway, 2) Skip this issue.

### TC-9026 -- CVE-2026-39330 openssl [rhtpa-2.2]

- **Current status:** Modified
- **Remediation tasks:** None (no Depend links)
- **Handling:** Excluded from Ready for QA -- no linked remediation tasks exist with type "Depend", so there is no remediation to verify.
- **Status note:** Modified is not a warning-triggering status. If selected for individual triage, proceed normally. The absence of linked remediation tasks may indicate triage was completed with a "Close as Not a Bug" recommendation, or remediation tasks were never created.
