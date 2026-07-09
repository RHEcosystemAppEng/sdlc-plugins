# Status-Aware Handling Decisions

## Query 1 Issues -- Untriaged

### TC-9001 (CVE-2026-40112) -- Status: New
- **Handling**: Proceed with full triage (default path for New status).
- No warning needed.

### TC-9002 (CVE-2026-40297) -- Status: New
- **Handling**: Proceed with full triage (default path for New status).
- No warning needed.

### TC-9003 (CVE-2026-40455) -- Status: In Progress
- **Handling**: **WARNING** -- This issue is already in `In Progress` status. It may be actively worked on by another engineer.
- If the user selects this issue, present the warning and ask:
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue
- Do not auto-triage without user confirmation.

### TC-9004 (CVE-2026-40518) -- Status: New
- **Handling**: Proceed with full triage (default path for New status).
- No warning needed.

## Query 2 Issues -- Triaged but still New

### TC-9010 (CVE-2026-39874) -- Status: New
- **Handling**: This issue was previously triaged (has `ai-cve-triaged` label) but remains in New status. It may need follow-up or re-triage. Present for engineer review.

## Query 3 Issues -- Ready for QA

### TC-9020 (CVE-2026-38901) -- Status: Modified
- **Handling**: All linked remediation Tasks are completed (TC-9021 Done, TC-9022 Closed). Ready for QA transition.
- **Suggestion**: Consider transitioning to ON_QA.

### TC-9023 (CVE-2026-39102) -- Status: In Progress
- **Handling**: Excluded from Ready for QA. Remediation task TC-9025 is still In Progress -- remediation is not yet complete.

### TC-9026 (CVE-2026-39330) -- Status: Modified
- **Handling**: Excluded from Ready for QA. No linked Tasks with type "Depend" exist -- no remediation to verify.
