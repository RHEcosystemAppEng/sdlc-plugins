# triage-security — Status-Aware Handling Decisions

These follow SKILL.md "Discovery mode → Status-aware handling" and Step 0.8. When an
issue is selected, its current status decides the path:

- **New** → run full triage (the default path)
- **In Progress / Code Review / QA** → warn: "This issue is already in `<status>`. It may be actively worked on." Then ask: (1) proceed with triage anyway, or (2) skip
- **Closed / Done / Resolved** → warn: "This issue is already closed." Then ask: (1) re-triage, or (2) skip
- Step 0.8: the assignment to the current user always happens. The transition to **Assigned** happens only when the issue is in **New**. For Assigned or any later status, the transition is skipped silently.
- If the user skips, go back to the discovery list or end the session.

## Per-issue decisions

| Issue | List | Status | Handling | Step 0.8 Assign | Step 0.8 Transition to Assigned |
|-------|------|--------|----------|-----------------|---------------------------------|
| TC-9001 | Untriaged | New | Full triage (default path), no warning | Yes | Yes (New → Assigned) |
| TC-9002 | Untriaged | New | Full triage (default path), no warning | Yes | Yes (New → Assigned) |
| TC-9004 | Untriaged | New | Full triage (default path), no warning | Yes | Yes (New → Assigned) |
| TC-9003 | Untriaged | In Progress | **Warn** and ask whether to proceed or skip | Yes (if proceeding) | No (already past New, skipped silently) |
| TC-9010 | Triaged but still New | New | Full triage path, flagged as stale (triaged but never actioned). Offer re-triage or follow-up | Yes | Yes (New → Assigned) |
| TC-9020 | Ready for QA | Modified | **Warn** and ask whether to proceed or skip. Main recommendation: transition to ON_QA instead of re-triaging | Yes (if proceeding) | No (already past New, skipped silently) |

## Details

### TC-9001 — CVE-2026-40112 (h2) [rhtpa-2.2] — New
Default path, no prompt. Assign to the current user and transition New → Assigned. Then
run Steps 1–8. The stream suffix `[rhtpa-2.2]` maps to stream **2.2.x**.

### TC-9002 — CVE-2026-40297 (serde_json) [rhtpa-2.1] — New
Default path, no prompt. Assign and transition New → Assigned, then run full triage.
The suffix `[rhtpa-2.1]` maps to stream **2.1.x**.

### TC-9004 — CVE-2026-40518 (ring) [rhtpa-2.2] — New
Default path, no prompt. Assign and transition New → Assigned, then run full triage.
The suffix maps to stream **2.2.x**.

### TC-9003 — CVE-2026-40455 (tokio) [rhtpa-2.2] — In Progress
The issue has not been triaged (no `ai-cve-triaged` label) but is already In Progress. Prompt:

> "This issue is already in `In Progress`. It may be actively worked on."
> 1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
> 2. Skip this issue

- If **proceed**: assign to the current user. Skip the Assigned transition silently because the status is past New. Run full triage. Step 7 (Concurrent Triage Detection) matters most here, since someone else may be working on it.
- If **skip**: go back to the discovery list.

### TC-9010 — CVE-2026-39874 (quinn-proto) [rhtpa-2.2] — New, already triaged
The status is New, so the default path applies and no status warning is needed. Because
it carries `ai-cve-triaged`, it is **flagged** as stale: it was triaged but never moved
forward. The engineer should check whether the earlier triage's remediation Tasks exist
and whether the issue only needs follow-up (moving it forward) or a full re-triage. If
re-triaging, assign and transition New → Assigned. During Step 4, reconcile with existing
or preemptive Tasks so duplicate remediation Tasks are not created.

### TC-9020 — CVE-2026-38901 (hyper) [rhtpa-2.2] — Modified, Ready for QA
All remediation Tasks are complete (TC-9021 Done, TC-9022 Closed). Recommended action:
**"Consider transitioning to ON_QA."** "Modified" is not named in the skill's status
list. It is a post-fix workflow status, later than In Progress, so it is handled like
the In Progress / Code Review / QA group:

> "This issue is already in `Modified`. It may be actively worked on."
> 1. Proceed with triage anyway (e.g., to verify the fix covers all versions)
> 2. Skip this issue

- If **proceed**: assign to the current user and skip the Assigned transition silently. Re-triaging should only confirm that the fix covers every affected stream.
- If **skip**: go back to the list. The ON_QA transition stays a suggestion for the engineer.

### Not selectable (excluded from Ready for QA)
- **TC-9023** (In Progress, triaged): remediation Task TC-9025 is still In Progress. No action; wait for remediation to finish.
- **TC-9026** (Modified, triaged): it has no "Depend" remediation Tasks, so there is nothing to verify. It is not listed. An engineer may want to look into why a triaged CVE is in Modified with no linked remediation.

## Empty-results fallback
Not triggered. Query 1 returned 4 issues, so the message "No untriaged Vulnerability
issues found in project TC." is not shown.
