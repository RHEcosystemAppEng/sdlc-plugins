# Status-Aware Handling Decisions

## Untriaged Issues (Query 1)

### TC-9001 — CVE-2026-40112 (Status: New)
- **Handling**: Proceed with full triage (default path)
- **Action**: Available for triage — New status indicates untriaged issue

### TC-9002 — CVE-2026-40297 (Status: New)
- **Handling**: Proceed with full triage (default path)
- **Action**: Available for triage — New status indicates untriaged issue

### TC-9003 — CVE-2026-40455 (Status: In Progress)
- **Handling**: ⚠️ Warning — "This issue is already in `In Progress`. It may be actively worked on."
- **Options presented**:
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue
- **Action**: Engineer must choose before proceeding. The In Progress status suggests another engineer may be actively working on this issue.

### TC-9004 — CVE-2026-40518 (Status: New)
- **Handling**: Proceed with full triage (default path)
- **Action**: Available for triage — New status indicates untriaged issue

## Triaged but still New (Query 2)

### TC-9010 — CVE-2026-39874 (Status: New)
- **Handling**: Flagged for follow-up — triaged (`ai-cve-triaged` label present) but never moved forward
- **Action**: May need re-triage or manual follow-up to determine why the issue was not actioned after initial triage

## Ready for QA Candidates (Query 3)

### TC-9020 — CVE-2026-38901 (Status: Modified)
- **Linked Tasks**: TC-9021 (Done), TC-9022 (Closed)
- **All remediation Tasks completed**: YES
- **Handling**: Ready for QA — suggest transitioning to ON_QA
- **Action**: Consider transitioning to ON_QA. All linked remediation Tasks have been completed.

### TC-9023 — CVE-2026-39102 (Status: In Progress)
- **Linked Tasks**: TC-9024 (Done), TC-9025 (In Progress)
- **All remediation Tasks completed**: NO — TC-9025 still In Progress
- **Handling**: Excluded from Ready for QA
- **Action**: Remediation is still in progress. Wait for TC-9025 to complete before considering QA transition.

### TC-9026 — CVE-2026-39330 (Status: Modified)
- **Linked Tasks**: None (no Depend links)
- **All remediation Tasks completed**: N/A — no linked remediation Tasks
- **Handling**: Excluded from Ready for QA
- **Action**: No remediation Tasks linked via "Depend" link type. Cannot verify remediation completion. May need investigation to determine if remediation tasks were created but not linked, or if remediation was handled differently.
