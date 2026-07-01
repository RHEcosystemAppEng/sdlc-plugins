# Status-Aware Handling Decisions

For each issue listed in the discovery results, the following status-aware handling applies per the triage-security skill's Discovery Mode protocol.

---

## Query 1: Untriaged Issues

### TC-9001 — Status: New — CVE-2026-40112
- **Handling**: Proceed with full triage (default path)
- **Action**: Present for full triage. This is an untriaged issue in New status — the standard triage flow (Steps 1 through 8) applies.

### TC-9002 — Status: New — CVE-2026-40297
- **Handling**: Proceed with full triage (default path)
- **Action**: Present for full triage. This is an untriaged issue in New status — the standard triage flow (Steps 1 through 8) applies.

### TC-9003 — Status: In Progress — CVE-2026-40455
- **Handling**: Warning — active work detected
- **Action**: This issue is already in `In Progress` status. It may be actively worked on. Before triaging, the engineer should be warned:

  > "This issue is already in `In Progress`. It may be actively worked on."
  >
  > Options:
  > 1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  > 2. Skip this issue

### TC-9004 — Status: New — CVE-2026-40518
- **Handling**: Proceed with full triage (default path)
- **Action**: Present for full triage. This is an untriaged issue in New status — the standard triage flow (Steps 1 through 8) applies.

---

## Query 2: Triaged but still New

### TC-9010 — Status: New — CVE-2026-39874
- **Handling**: Flagged for follow-up
- **Action**: This issue has the `ai-cve-triaged` label but remains in New status. It was triaged but never moved forward. The engineer should investigate whether:
  - The triage outcome was "close" but the close was not executed
  - Remediation tasks were created but the Vulnerability issue was not transitioned
  - Re-triage is needed due to changed circumstances

---

## Query 3: Ready for QA

### TC-9020 — Status: Modified — CVE-2026-38901
- **Handling**: Ready for QA transition
- **Action**: All linked remediation Tasks are completed (TC-9021 Done, TC-9022 Closed). Consider transitioning to ON_QA.

### TC-9023 — Status: In Progress — CVE-2026-39102
- **Handling**: Excluded from Ready for QA
- **Action**: TC-9025 is still In Progress — remediation is not complete. This issue cannot transition to ON_QA until all linked remediation Tasks are Done or Closed.

### TC-9026 — Status: Modified — CVE-2026-39330
- **Handling**: Excluded from Ready for QA
- **Action**: No linked Tasks with type "Depend" exist. Without remediation tasks to verify, this issue cannot be transitioned to ON_QA. The engineer should investigate whether remediation tasks were created but not linked, or whether the triage outcome was incomplete.

---

## Summary

| Issue | Status | Handling | Decision |
|-------|--------|----------|----------|
| TC-9001 | New | Full triage | Present for triage |
| TC-9002 | New | Full triage | Present for triage |
| TC-9003 | In Progress | Warning: active work | Warn engineer, ask to proceed or skip |
| TC-9004 | New | Full triage | Present for triage |
| TC-9010 | New (triaged) | Follow-up flag | May need re-triage or action |
| TC-9020 | Modified | Ready for QA | Suggest transition to ON_QA |
| TC-9023 | In Progress | Excluded | TC-9025 still In Progress |
| TC-9026 | Modified | Excluded | No Depend links |
