# triage-security — Status-Aware Handling Decisions

Per SKILL.md "Status-aware handling" (Inputs → Discovery mode), applied when the engineer selects an issue from the discovery list:

- **New** → proceed with full triage (default path). Step 0.8 assigns to current user and transitions New → Assigned (transition discovered dynamically via `get_transitions`, never hardcoded).
- **In Progress / Code Review / QA** → warn "This issue is already in `<status>`. It may be actively worked on." and ask: (1) proceed with triage anyway, or (2) skip.
- **Closed / Done / Resolved** → warn "This issue is already closed." and ask: (1) re-triage, or (2) skip.
- On skip → return to the discovery list or end the session.
- No Jira mutation happens without explicit engineer confirmation.

## Per-issue decisions

| Issue | List | Status | Handling | Step 0.8 behavior (if triage proceeds) |
|---|---|---|---|---|
| TC-9001 | Untriaged | New | Proceed with full triage (default path) | Assign to current user; transition New → Assigned |
| TC-9002 | Untriaged | New | Proceed with full triage (default path) | Assign to current user; transition New → Assigned |
| TC-9004 | Untriaged | New | Proceed with full triage (default path) | Assign to current user; transition New → Assigned |
| TC-9003 | Untriaged | In Progress | Warn: "This issue is already in `In Progress`. It may be actively worked on." Ask: 1) Proceed with triage anyway (e.g., verify version impact / update Affects Versions), 2) Skip | If proceed: assign to current user; skip transition silently (already past Assigned) |
| TC-9010 | Triaged but still New | New | Flagged as stale (triaged, never actioned). Status is New → default full-triage path is available as a re-triage; engineer should confirm re-triage since `ai-cve-triaged` is already present (earlier triage summary comment likely exists) | Assign to current user; transition New → Assigned |
| TC-9020 | Ready for QA | Modified | Not a triage target — all Depend remediation Tasks (TC-9021 Done, TC-9022 Closed) complete. Suggest: "Consider transitioning to ON_QA." Transition only on explicit engineer approval. If engineer instead selects it for triage, `Modified` is a post-Assigned active status not explicitly listed; treat like the In Progress branch (warn + proceed/skip) | If proceed: assign; skip transition (already past Assigned) |
| TC-9023 | Excluded from Ready for QA (Query 3 candidate) | In Progress | Not listed for QA: TC-9025 still In Progress. If selected: warn "already in `In Progress`", ask proceed/skip | If proceed: assign; skip transition |
| TC-9026 | Excluded from Ready for QA (Query 3 candidate) | Modified | Not listed for QA: no Depend-linked remediation Tasks to verify. If selected: treat as active post-Assigned status → warn + proceed/skip. Worth engineer follow-up since it is Modified with no remediation tasks | If proceed: assign; skip transition |

## Notes

- No issues in any list are in Closed / Done / Resolved status, so the "already closed → re-triage or skip" branch is not triggered for any listed issue.
- `Modified` is not explicitly named in the status-aware handling rules; it is mapped conservatively to the "actively worked on" warn-and-ask branch rather than silently proceeding.
- Release Jira summary (Query 4) has no supplied results, so no release-level handling decisions are made.
