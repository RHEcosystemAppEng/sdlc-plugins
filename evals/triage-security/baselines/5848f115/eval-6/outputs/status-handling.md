# Status-Aware Handling Decisions

Per SKILL.md Discovery Mode, each issue's current Jira status determines the handling path when selected for triage. Below are the status-aware decisions for every issue surfaced in the discovery queries.

---

## Untriaged Issues (Query 1)

### TC-9001 -- CVE-2026-40112 h2 [rhtpa-2.2]
- **Status**: New
- **Handling**: Proceed with full triage (default path). New status indicates this issue has not been triaged or actioned. Run Steps 0 through 8 in sequence.

### TC-9002 -- CVE-2026-40297 serde_json [rhtpa-2.1]
- **Status**: New
- **Handling**: Proceed with full triage (default path). New status indicates this issue has not been triaged or actioned. Run Steps 0 through 8 in sequence.

### TC-9003 -- CVE-2026-40455 tokio [rhtpa-2.2]
- **Status**: In Progress
- **Handling**: Warn the user before proceeding. This issue is already in "In Progress" status, which means it may be actively worked on by another engineer.
  - Present warning: "This issue is already in In Progress. It may be actively worked on."
  - Offer two options:
    1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
    2. Skip this issue
  - If the user chooses to skip, return to the discovery list or end the session.

### TC-9004 -- CVE-2026-40518 ring [rhtpa-2.2]
- **Status**: New
- **Handling**: Proceed with full triage (default path). New status indicates this issue has not been triaged or actioned. Run Steps 0 through 8 in sequence.

---

## Triaged but still New (Query 2)

### TC-9010 -- CVE-2026-39874 quinn-proto [rhtpa-2.2]
- **Status**: New
- **Labels**: includes `ai-cve-triaged`
- **Handling**: This issue has been triaged previously (it carries the `ai-cve-triaged` label) but was never moved out of New status. This is a stale issue that may need follow-up or re-triage. Since its status is New, the default triage path applies if selected -- proceed with full triage. However, the engineer should consider why this issue was triaged but never actioned:
  - Were remediation tasks created but not linked?
  - Was the issue closed as Not a Bug but the status transition failed?
  - Does it need re-triage with updated data?

---

## Ready for QA Candidates (Query 3)

### TC-9020 -- CVE-2026-38901 hyper [rhtpa-2.2]
- **Status**: Modified
- **Linked Tasks**: TC-9021 (Done), TC-9022 (Closed) -- all completed
- **Handling**: This is not a triage candidate but a QA-readiness candidate. All linked remediation tasks are complete (Done or Closed). The recommended action is to transition this issue to ON_QA status. No triage steps are needed; instead, verify remediation completeness and transition the Vulnerability issue.

### TC-9023 -- CVE-2026-39102 rustls [rhtpa-2.1]
- **Status**: In Progress
- **Linked Tasks**: TC-9024 (Done), TC-9025 (In Progress) -- not all completed
- **Handling**: Not ready for QA -- TC-9025 is still In Progress. If selected for triage, warn the user: "This issue is already in In Progress. It may be actively worked on."
  - Offer two options:
    1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
    2. Skip this issue
  - Remediation is still in progress; transitioning to ON_QA is not appropriate.

### TC-9026 -- CVE-2026-39330 openssl [rhtpa-2.2]
- **Status**: Modified
- **Linked Tasks**: None with type "Depend"
- **Handling**: Not ready for QA -- no linked remediation tasks exist with link type "Depend", so there is no remediation work to verify. If selected for triage, the Modified status falls under the "In Progress / Code Review / QA" handling path -- warn the user: "This issue is already in Modified. It may be actively worked on."
  - Offer two options:
    1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
    2. Skip this issue
  - The absence of remediation tasks may indicate the issue needs investigation -- was triage completed but task creation skipped or failed?

---

## Summary Table

| Issue | Status | Query Source | Handling Decision |
|-------|--------|-------------|-------------------|
| TC-9001 | New | Untriaged | Full triage (default path) |
| TC-9002 | New | Untriaged | Full triage (default path) |
| TC-9003 | In Progress | Untriaged | Warn: may be actively worked on; ask to proceed or skip |
| TC-9004 | New | Untriaged | Full triage (default path) |
| TC-9010 | New (triaged) | Triaged-but-New | Full triage if selected; flag as stale for follow-up |
| TC-9020 | Modified | Ready for QA | All tasks completed; recommend transition to ON_QA |
| TC-9023 | In Progress | Ready for QA (excluded) | Warn: actively worked on; remediation incomplete |
| TC-9026 | Modified | Ready for QA (excluded) | Warn: may be actively worked on; no remediation tasks found |
