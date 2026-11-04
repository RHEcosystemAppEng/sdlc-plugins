# triage-security — Status-Aware Handling Decisions

Per SKILL.md "Status-aware handling": when an issue is selected, its current Jira status determines the path.

- **New** → proceed with full triage (default path)
- **In Progress / Code Review / QA** → warn "This issue is already in `<status>`. It may be actively worked on." and ask: (1) proceed with triage anyway, or (2) skip
- **Closed / Done / Resolved** → warn "This issue is already closed." and ask: (1) re-triage, or (2) skip

On skip, return to the discovery list or end the session. No Jira mutation (including Step 0.8 assign/transition) happens before the engineer confirms.

## Per-Issue Decisions

| Issue | List | Status | CVE | Stream scope (from suffix) | Handling decision |
|---|---|---|---|---|---|
| TC-9001 | Untriaged | New | CVE-2026-40112 | `[rhtpa-2.2]` → 2.2.x | **Proceed with full triage.** Step 0.8: assign to current user and transition New → Assigned (target resolved dynamically via `get_transitions`, after confirmation). |
| TC-9002 | Untriaged | New | CVE-2026-40297 | `[rhtpa-2.1]` → 2.1.x | **Proceed with full triage.** Step 0.8: assign + transition New → Assigned. |
| TC-9004 | Untriaged | New | CVE-2026-40518 | `[rhtpa-2.2]` → 2.2.x | **Proceed with full triage.** Step 0.8: assign + transition New → Assigned. |
| TC-9003 | Untriaged | In Progress | CVE-2026-40455 | `[rhtpa-2.2]` → 2.2.x | **Warn and ask.** "This issue is already in `In Progress`. It may be actively worked on." Options: (1) proceed with triage anyway (e.g., verify version impact / update Affects Versions), (2) skip. If proceeding: Step 0.8 assigns to current user but **skips the Assigned transition** (already past Assigned). |
| TC-9010 | Triaged but still New (flagged) | New | CVE-2026-39874 | `[rhtpa-2.2]` → 2.2.x | **New → full triage path is available**, but flagged as stale: already carries `ai-cve-triaged`. Engineer should review existing triage comment/remediation tasks first; re-triage if needed. If re-triaged: assign + transition New → Assigned; the Step 4 reconciliation should check existing remediation tasks to avoid duplicates. |
| TC-9020 | Ready for QA | Modified | CVE-2026-38901 | `[rhtpa-2.2]` → 2.2.x | **Not a triage candidate.** Already triaged; all Depend-linked remediation Tasks (TC-9021 Done, TC-9022 Closed) are complete. Recommendation: "Consider transitioning to ON_QA." (Requires explicit engineer confirmation; no automatic transition.) Modified is not listed in the status-aware rules; if the engineer selects it for re-triage, treat it as an active/post-work status: warn and offer proceed or skip, and skip the Assigned transition. |

### Excluded from Ready for QA (shown for completeness, not listed as actionable)

| Issue | Status | Reason | Decision |
|---|---|---|---|
| TC-9023 | In Progress | TC-9025 still In Progress | No action: remediation still under way. If selected, apply the In Progress warning (proceed or skip). |
| TC-9026 | Modified | No Depend-linked Tasks | No action: no remediation to verify. Worth a manual look, because it is Modified and triaged but has no remediation tasks linked. |

## Summary

- **Ready for full triage (New):** TC-9001, TC-9002, TC-9004
- **Needs a warning and engineer choice (In Progress):** TC-9003
- **Stale, flagged for follow-up/re-triage:** TC-9010
- **ON_QA transition candidate:** TC-9020
- **Closed / Done / Resolved issues in the lists:** none, so the "already closed" path does not apply to any listed issue.
