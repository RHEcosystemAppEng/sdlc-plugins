# triage-security — Status-Aware Handling Decisions

The SKILL.md "Status-aware handling" rules apply when the engineer selects an issue from the discovery list:

- **New**: go straight to full triage (the default path).
- **In Progress / Code Review / QA**: warn "This issue is already in `<status>`. It may be actively worked on." Then offer two options: (1) proceed with triage anyway or (2) skip.
- **Closed / Done / Resolved**: warn "This issue is already closed." Then offer two options: (1) re-triage or (2) skip.
- If the engineer skips, go back to the discovery list or end the session.

Step 0.8 (assign to current user and transition to Assigned) runs only after the engineer confirms triage. The transition to Assigned happens only when the issue is in **New**. For any issue already in Assigned or a later status, the transition is skipped silently, but the assignment still happens.

## Per-issue decisions

| # | Issue | List | Status | Handling | Warning / prompt | Step 0.8 behavior if triaged |
|---|---|---|---|---|---|---|
| 1 | TC-9001 | Untriaged | New | **Full triage (default path)** | None | Assign to current user, then transition New → Assigned |
| 2 | TC-9002 | Untriaged | New | **Full triage (default path)** | None | Assign, then transition New → Assigned |
| 3 | TC-9004 | Untriaged | New | **Full triage (default path)** | None | Assign, then transition New → Assigned |
| 4 | TC-9003 | Untriaged | In Progress | **Warn and ask: proceed or skip** | "This issue is already in `In Progress`. It may be actively worked on." Options: 1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions) 2. Skip this issue | Assign if the engineer proceeds; **skip the transition** (already past Assigned) |
| 5 | TC-9010 | Triaged but still New | New | **Full triage path, flagged as a re-triage candidate.** Status is New, so no status warning, but the issue already carries `ai-cve-triaged` and was never actioned | Flagged as stale: review the earlier triage comment and decide whether to follow up or re-triage | Assign, then transition New → Assigned |
| 6 | TC-9020 | Ready for QA | Modified | **No triage needed. Suggest "Consider transitioning to ON_QA."** Every Depend Task is done (TC-9021 Done, TC-9022 Closed). If the engineer still selects it, Modified is a post-triage, actively-worked state, so treat it like the In Progress/QA rule: warn and ask proceed or skip | "This issue is already in `Modified`. It may be actively worked on." | Assign only; skip the transition |
| — | TC-9023 | Excluded (Query 3) | In Progress | Not listed. Remediation is still in progress (TC-9025 In Progress). No action | n/a (warning would apply if opened directly by key) | n/a |
| — | TC-9026 | Excluded (Query 3) | Modified | Not listed. No Depend-linked remediation Tasks, so there is nothing to verify for QA. No action | n/a | n/a |

## Notes on stream scope (preview for Step 1)

The bracketed suffixes map to the configured Version Streams as follows:

| Issue(s) | Suffix | Stream |
|---|---|---|
| TC-9001, TC-9003, TC-9004, TC-9010, TC-9020 | `[rhtpa-2.2]` | 2.2.x |
| TC-9002 | `[rhtpa-2.1]` | 2.1.x |

All suffixes match a configured stream, so no engineer confirmation of stream scope is expected.

## Summary

- **Ready for full triage now:** TC-9001, TC-9002, TC-9004.
- **Needs engineer decision before triage:** TC-9003 (In Progress: proceed or skip).
- **Needs follow-up (stale triaged):** TC-9010.
- **Suggest ON_QA transition:** TC-9020.
- **No Closed/Done/Resolved issues** came back in any list, so the "already closed: re-triage or skip" branch does not apply to this run.
- No Jira mutations were made. Discovery mode is read-only, and every later mutation needs explicit engineer confirmation.
