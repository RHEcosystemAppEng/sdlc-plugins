# triage-security — Status-Aware Handling Decisions

These rules come from SKILL.md, "Inputs > Discovery mode > Status-aware handling". They apply when the engineer selects an issue from the discovery list:

- **New**: go straight to full triage (the default path, Steps 0.8 through 8).
- **In Progress / Code Review / QA**: warn "This issue is already in `<status>`. It may be actively worked on." and offer two choices: (1) proceed with triage anyway, or (2) skip.
- **Closed / Done / Resolved**: warn "This issue is already closed." and offer two choices: (1) re-triage, or (2) skip.
- A skip returns to the discovery list or ends the session.

Step 0.8 also depends on status. For a **New** issue, assign it to the current user and transition it to Assigned. For any later status, assign only and skip the transition silently. The transition is found dynamically through `get_transitions`, never by a hardcoded ID.

Every Jira mutation still needs explicit engineer confirmation, including assignment, transitions, labels, and comments.

---

## Per-issue decisions

| Issue | List | Status | Handling path | Warning shown? | Step 0.8 behavior |
|-------|------|--------|---------------|----------------|-------------------|
| TC-9001 | Untriaged | New | Full triage | No | Assign to current user and transition New to Assigned |
| TC-9002 | Untriaged | New | Full triage | No | Assign and transition New to Assigned |
| TC-9004 | Untriaged | New | Full triage | No | Assign and transition New to Assigned |
| TC-9003 | Untriaged | In Progress | Warn, then ask: proceed or skip | Yes | If proceeding: assign only, skip transition |
| TC-9010 | Triaged but still New | New | Flagged stale. Offer re-triage (full triage path) | Stale flag (not a status warning) | If re-triaging: assign and transition New to Assigned |
| TC-9020 | Ready for QA | Modified | Not a triage target. Suggest ON_QA transition | Treated as active-work status if selected for triage | If re-triage is chosen: assign only, skip transition |
| TC-9023 | (excluded from Ready for QA) | In Progress | Not listed. If selected by key: warn, then proceed/skip | Yes | Assign only, skip transition |
| TC-9026 | (excluded from Ready for QA) | Modified | Not listed. If selected by key: warn, then proceed/skip | Yes | Assign only, skip transition |

---

## Details

### TC-9001: CVE-2026-40112 (h2), New, stream 2.2.x
- Status New, so take the **default full-triage path** with no warning.
- Step 0.8: after confirmation, assign to the current user and transition to Assigned.
- Stream scope: suffix `[rhtpa-2.2]` maps to configured stream `2.2.x`, so the issue is scoped. Step 2 still checks all streams (2.1.x and 2.2.x) as Rule 4 requires. Case A cross-stream handling applies if 2.1.x is also affected.
- Ecosystem: Cargo (Rust crate), which means 2 remediation tasks per affected stream.

### TC-9002: CVE-2026-40297 (serde_json), New, stream 2.1.x
- Status New, so take the **default full-triage path** with no warning.
- Step 0.8: assign and transition to Assigned.
- Scoped to `2.1.x` via `[rhtpa-2.1]`. If 2.2.x is affected too, it goes through Case A (cross-stream comment, plus preemptive tasks if 2.2.x has no CVE Jira of its own).
- Ecosystem: Cargo.

### TC-9004: CVE-2026-40518 (ring), New, stream 2.2.x
- Status New, so take the **default full-triage path** with no warning.
- Step 0.8: assign and transition to Assigned.
- Scoped to `2.2.x`. Ecosystem: Cargo.

### TC-9003: CVE-2026-40455 (tokio), In Progress, stream 2.2.x
- Status In Progress, so the **active-work warning applies**:
  > "This issue is already in `In Progress`. It may be actively worked on."
  >
  > 1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  > 2. Skip this issue
- Wait for the engineer's choice. Do not continue automatically.
- If **Proceed**: Step 0.8 assigns the issue to the current user (after confirmation) and **skips the transition to Assigned** because the issue is already past New. The full triage then continues. Step 7 (concurrent triage detection) matters here because someone else may already be remediating.
- If **Skip**: go back to the discovery list.
- Observation: it is In Progress without the `ai-cve-triaged` label, so work started without AI triage. Version-impact verification and Affects Versions correction may still add value.

### TC-9010: CVE-2026-39874 (quinn-proto), New, triaged but still New
- Listed under **Triaged but still New** and flagged as stale. It was triaged (label present) but never moved forward.
- Status is New, so the status rule allows the full-triage path with no status warning. Because it already has `ai-cve-triaged`, tell the engineer this would be a **re-triage** and recommend checking first:
  - whether remediation tasks were created and linked (Depend), and
  - whether the earlier triage closed it as Not a Bug without the transition being applied.
- If re-triage goes ahead: Step 0.8 assigns and transitions New to Assigned. Step 4 duplicate and reconciliation checks should find any remediation tasks created earlier, so they are not duplicated. The `ai-cve-triaged` label is already present and is not added again.

### TC-9020: CVE-2026-38901 (hyper), Modified, Ready for QA
- Every Depend-linked remediation Task is finished (TC-9021 Done, TC-9022 Closed).
- Decision: **suggest "Consider transitioning to ON_QA."** Do not re-triage. The ON_QA transition is a Jira mutation, so it needs explicit engineer confirmation and is not executed here.
- If the engineer selects it for triage anyway, Modified is a post-New active-work status. Show the "already in `Modified`" warning with proceed/skip, and skip the Assigned transition.

### TC-9023: CVE-2026-39102 (rustls), In Progress, excluded from Ready for QA
- Excluded because TC-9025 is still In Progress, so remediation is ongoing. No action is suggested.
- If selected by key: show the In Progress warning with proceed/skip, and Step 0.8 assigns only.

### TC-9026: CVE-2026-39330 (openssl), Modified, excluded from Ready for QA
- Excluded because it has no Depend-linked remediation Tasks, so there is nothing to verify.
- It is still worth a manual look: the issue is triaged and in Modified but has no remediation links. It may have been dedup'd onto another CVE's task (Step 7.5.3) or remediated outside the link topology. If re-triaged by key: show the "already in `Modified`" warning with proceed/skip, and Step 0.8 assigns only. Ecosystem is likely RPM (openssl system package), which means 1 Konflux task per stream if remediation is needed.

---

## Summary

- **Ready for full triage with no warning:** TC-9001, TC-9002, TC-9004
- **Needs a warning and proceed/skip choice before triage:** TC-9003 (In Progress)
- **Stale, re-triage recommended after review:** TC-9010
- **Ready for QA, suggest ON_QA transition:** TC-9020
- **Excluded, no action:** TC-9023 (remediation open), TC-9026 (no Depend links; flagged for manual review)
- **No closed, done, or resolved issues** came back in any list, so the "already closed / re-triage or skip" path is not triggered for this set.

No Jira mutations were made. Each action above needs explicit engineer confirmation in an interactive run.
