# Status-Aware Handling Decisions

Applied per the triage-security skill's "Status-aware handling" rules (Inputs → Discovery mode) and Step 0.8 (Assign and Transition to Assigned). These are the decisions that would apply when the engineer selects each issue; no Jira calls were made.

Rules:
- **New** → proceed with full triage (default path).
- **In Progress / Code Review / QA** → warn: "This issue is already in `<status>`. It may be actively worked on." Ask: (1) proceed with triage anyway, or (2) skip.
- **Closed / Done / Resolved** → warn: "This issue is already closed." Ask: (1) re-triage, or (2) skip.
- Step 0.8: always assign to current user; transition to "Assigned" (discovered via `get_transitions`, never hardcoded) only if the issue is in New. Already in Assigned or later → skip transition silently.
- Skipping returns to the discovery list.

## Summary

| Issue | List | Status | Decision | Step 0.8 assign | Step 0.8 transition to Assigned |
|-------|------|--------|----------|-----------------|------------------|
| TC-9001 | Untriaged | New | Proceed with full triage | Yes | Yes |
| TC-9002 | Untriaged | New | Proceed with full triage | Yes | Yes |
| TC-9004 | Untriaged | New | Proceed with full triage | Yes | Yes |
| TC-9003 | Untriaged | In Progress | Warn + ask (proceed / skip) | Yes, if proceeding | No — already past New, skip silently |
| TC-9010 | Triaged but still New | New | Flag as stale; proceed with full (re-)triage | Yes | Yes |
| TC-9020 | Ready for QA | Modified | Not a triage target; suggest ON_QA transition. If selected for re-triage: warn + ask | Yes, if re-triaging | No — past New |
| TC-9023 | Excluded from Ready for QA | In Progress | No action surfaced; if selected: warn + ask (proceed / skip) | Yes, if proceeding | No — past New |
| TC-9026 | Excluded from Ready for QA | Modified | No action surfaced; flag missing remediation Tasks. If selected: warn + ask | Yes, if proceeding | No — past New |

## Per-issue Detail

### TC-9001 — CVE-2026-40112 (h2, rhtpa-2.2) — New
Default path: full 8-step triage. Assign to current user, then transition New → Assigned.

### TC-9002 — CVE-2026-40297 (serde_json, rhtpa-2.1) — New
Default path: full triage. Assign + transition to Assigned.

### TC-9004 — CVE-2026-40518 (ring, rhtpa-2.2) — New
Default path: full triage. Assign + transition to Assigned.

### TC-9003 — CVE-2026-40455 (tokio, rhtpa-2.2) — In Progress
Unusual combination: no `ai-cve-triaged` label but already In Progress. Warn:
> "This issue is already in `In Progress`. It may be actively worked on."

Options:
1. Proceed with triage anyway (e.g., verify version impact or update Affects Versions)
2. Skip this issue

If proceeding: assign to current user (records the triager) but skip the Assigned transition silently (already beyond New). If skipped: return to discovery list.

### TC-9010 — CVE-2026-39874 (quinn-proto, rhtpa-2.2) — New (triaged, stale)
Status New → status rule says proceed with full triage. Because it already carries `ai-cve-triaged`, flag it to the engineer as stale (triaged on/after 2026-05-28 but never actioned) — likely needs follow-up or re-triage, e.g. check whether remediation Tasks were created and whether the Assigned transition was missed. Assign + transition New → Assigned.

### TC-9020 — CVE-2026-38901 (hyper, rhtpa-2.2) — Modified, Ready for QA
All Depend-linked remediation Tasks completed (TC-9021 Done, TC-9022 Closed). Recommendation: "Consider transitioning to ON_QA." Not a candidate for fresh triage. `Modified` is a post-development status not explicitly listed in the rules; it is treated like the "actively worked on" group (In Progress / Code Review / QA): if the engineer selects it for triage, warn and offer proceed / skip. No Assigned transition (past New).

### TC-9023 — CVE-2026-39102 (rustls, rhtpa-2.1) — In Progress
Excluded from Ready for QA because TC-9025 is still In Progress (TC-9024 Done). No action recommended; remediation ongoing. If selected: warn ("already in `In Progress`"), offer proceed / skip. No Assigned transition.

### TC-9026 — CVE-2026-39330 (openssl, rhtpa-2.2) — Modified
Excluded from Ready for QA: no "Depend"-linked remediation Tasks, so there is nothing to verify. Worth flagging: it is triaged and in Modified with no linked remediation, so the engineer may want to check whether remediation Tasks are missing or the link type is wrong. If selected: warn + ask (proceed / skip). No Assigned transition.

## Notes
- No issues are in Closed / Done / Resolved, so the re-triage prompt doesn't apply to any listed issue.
- Transition IDs are discovered at runtime via `jira.get_transitions`; Vulnerability issues use a different workflow from Tasks.
