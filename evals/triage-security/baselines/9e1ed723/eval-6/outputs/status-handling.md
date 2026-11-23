# triage-security — Status-Aware Handling Decisions

This file applies the SKILL.md "Status-aware handling" rules to each listed issue. The rules run when the engineer selects an issue:

- **New**: go straight to full triage (the default path).
- **In Progress / Code Review / QA**: warn "This issue is already in `<status>`. It may be actively worked on." Then ask: (1) proceed with triage anyway, or (2) skip.
- **Closed / Done / Resolved**: warn "This issue is already closed." Then ask: (1) re-triage, or (2) skip.
- If the engineer skips, return to the discovery list or end the session.

The skill makes no Jira mutation at the discovery or selection stage. Step 0.8 (assignment and the transition to Assigned) runs only after an issue is selected and confirmed. Every later Jira mutation still needs explicit engineer confirmation.

| Issue | List | Status | Handling decision |
|---|---|---|---|
| TC-9001 | Untriaged | New | **Full triage (default path).** No warning. Step 0.8 assigns the issue to the current user and moves it New to Assigned. Stream scope is `[rhtpa-2.2]`, which maps to stream `2.2.x`. |
| TC-9002 | Untriaged | New | **Full triage (default path).** No warning. Step 0.8 assigns the issue and moves it New to Assigned. Stream scope is `[rhtpa-2.1]`, which maps to stream `2.1.x`. |
| TC-9003 | Untriaged | In Progress | **Warn and ask.** "This issue is already in `In Progress`. It may be actively worked on." Options: (1) proceed with triage anyway, for example to verify version impact or update Affects Versions, or (2) skip. If the engineer proceeds, Step 0.8 still assigns the issue to the current user but skips the transition to Assigned, because the issue is already past Assigned. If the engineer skips, return to the discovery list. Stream scope is `[rhtpa-2.2]`, which maps to `2.2.x`. |
| TC-9004 | Untriaged | New | **Full triage (default path).** No warning. Step 0.8 assigns the issue and moves it New to Assigned. Stream scope is `[rhtpa-2.2]`, which maps to `2.2.x`. |
| TC-9010 | Triaged but still New | New | **Status New means the full triage path is allowed.** It is flagged because it already has the `ai-cve-triaged` label but was never actioned. Suggest follow-up or re-triage. If selected, run full triage as a re-triage: Step 0.8 assigns it and moves it New to Assigned. Steps 4 and 6 should detect existing remediation or sibling links so that duplicate tasks are not created. Stream scope is `[rhtpa-2.2]`, which maps to `2.2.x`. |
| TC-9020 | Ready for QA | Modified | **Do not re-triage. Suggest moving it to ON_QA.** All Depend Tasks (TC-9021 Done, TC-9022 Closed) are finished. Recommend "Consider transitioning to ON_QA". Any transition needs explicit engineer confirmation. Modified is not in the warn lists (In Progress/Code Review/QA or Closed/Done/Resolved). It is a post-triage state, so if the engineer selects it for triage anyway, warn that it is already actively progressed and ask to proceed or skip. In that case Step 0.8 skips the transition to Assigned because the issue is already past it. |
| TC-9023 | Excluded from Ready for QA (shown for context) | In Progress | **Not shown as Ready for QA**, because TC-9025 is still In Progress. If selected, use the In Progress rule: warn "This issue is already in `In Progress`. It may be actively worked on." and ask to proceed or skip. Assignment still happens and the transition is skipped. |
| TC-9026 | Excluded from Ready for QA (shown for context) | Modified | **Not shown as Ready for QA**, because it has no Depend-linked remediation Tasks. It is triaged and in Modified with nothing to verify, so flag it for manual review. It may have been closed out by another path, or its remediation links may be missing. If selected, warn that it is already past New and ask to proceed with re-triage or skip. The transition to Assigned is skipped. |

## Summary

- **Ready for immediate full triage:** TC-9001, TC-9002, TC-9004 (all New, untriaged).
- **Warning and confirmation required before triage:** TC-9003 (In Progress).
- **Flagged for follow-up or re-triage:** TC-9010 (triaged but still New).
- **ON_QA transition candidate:** TC-9020.
- **Excluded or needs manual review:** TC-9023 (remediation still in progress), TC-9026 (no Depend remediation links).
- No issue in the results is Closed, Done or Resolved, so the "already closed / re-triage" prompt does not apply to any listed issue.
