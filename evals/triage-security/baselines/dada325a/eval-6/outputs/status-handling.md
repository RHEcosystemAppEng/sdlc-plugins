# triage-security: Status-Aware Handling Decisions

These decisions follow the status-aware handling rules in SKILL.md (Inputs, "Status-aware handling"):

- **New**: proceed with full triage (the default path).
- **In Progress / Code Review / QA**: warn "This issue is already in `<status>`. It may be actively worked on." Then ask: (1) proceed with triage anyway, or (2) skip.
- **Closed / Done / Resolved**: warn "This issue is already closed." Then ask: (1) re-triage, or (2) skip.
- If you choose to skip, the skill returns to the discovery list or ends the session.

These decisions only take effect after you select an issue. Discovery mode itself makes no Jira changes. Step 0.8 (assign and transition to Assigned) runs only after an issue is selected and you confirm. It performs the Assigned transition only for issues in **New** and skips it for issues already in Assigned or a later status. The assignment itself always happens after you confirm.

## Per-issue decisions

| Issue | List | Status | Category | Decision |
|---|---|---|---|---|
| TC-9001 | Untriaged | New | New | **Proceed with full triage.** Step 0.8 assigns the issue and transitions it New -> Assigned, then Steps 1 to 8 run. Scope: stream 2.2.x (`[rhtpa-2.2]`). |
| TC-9002 | Untriaged | New | New | **Proceed with full triage.** Step 0.8 assigns and transitions to Assigned. Scope: stream 2.1.x (`[rhtpa-2.1]`). |
| TC-9003 | Untriaged | In Progress | Active work | **Warn and ask.** "This issue is already in `In Progress`. It may be actively worked on." Options: (1) proceed with triage anyway, for example to verify version impact or update Affects Versions; (2) skip. If you proceed, Step 0.8 assigns the issue but **skips** the Assigned transition because the status is already past Assigned. Scope: 2.2.x. |
| TC-9004 | Untriaged | New | New | **Proceed with full triage.** Step 0.8 assigns and transitions to Assigned. Scope: 2.2.x (`[rhtpa-2.2]`). |
| TC-9010 | Triaged but still New | New | New (stale) | **Flagged as stale.** Already labelled `ai-cve-triaged` but never actioned. Because the status is New, selecting it takes the full triage (re-triage) path. Before acting, check its existing triage comment and any remediation Tasks: Step 4 duplicate/reconciliation and Step 7.5.3 deduplication should find earlier artifacts and avoid creating duplicate Tasks. Step 0.8 assigns and transitions to Assigned. Scope: 2.2.x. |
| TC-9020 | Ready for QA | Modified | Remediation complete | **No re-triage needed. Suggest "Consider transitioning to ON_QA."** All Depend-linked Tasks are complete (TC-9021 Done, TC-9022 Closed). "Modified" is a post-fix, pre-QA state. If you explicitly select it for re-triage, treat it like an active-work status: warn and offer proceed or skip. Any ON_QA transition needs your explicit confirmation and uses a transition discovered dynamically with `get_transitions`. |
| TC-9023 | Excluded from Ready for QA | In Progress | Active work | **Not listed for QA.** TC-9025 is still In Progress, so remediation is ongoing. No action is suggested. If you select it, warn "already in `In Progress`" and offer proceed or skip. Scope: 2.1.x. |
| TC-9026 | Excluded from Ready for QA | Modified | Anomaly | **Not listed for QA.** It has no Depend-linked remediation Tasks, so there is nothing to verify. Flag for your review: the issue is triaged and in Modified but has no tracked remediation. The fix may have been handled outside the skill, or the links may be missing. If you select it, warn that it is already in `Modified` and offer proceed (re-triage to confirm version impact and create or link remediation) or skip. |

## Summary

- **Full triage, no warning:** TC-9001, TC-9002, TC-9004, and TC-9010. TC-9010 is a stale re-triage, so check its existing artifacts first.
- **Warn and confirm proceed or skip:** TC-9003 (In Progress). This also applies to TC-9023, TC-9020, and TC-9026 if you select them.
- **ON_QA candidate:** TC-9020.
- **Needs review:** TC-9026 (Modified with no remediation links).
- **No issues are in Closed, Done, or Resolved status**, so the re-triage-closed prompt does not apply to any listed issue.
- No Jira changes were made. Each later action needs your explicit confirmation.
