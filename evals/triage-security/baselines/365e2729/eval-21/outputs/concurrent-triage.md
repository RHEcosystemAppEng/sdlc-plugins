# Step 7 – Concurrent Triage Detection: TC-8020

## Prerequisite check

| Check | Result |
|-------|--------|
| Upstream Affected Component custom field configured? | YES — `customfield_10632` (assumed configured in Security Configuration per task) |
| Field value on TC-8020 | `quinn-proto` (non-empty) -> step runs |

## JQL search (simulated — not executed against Jira)

```
project = TC AND issuetype = 10024 AND cf[10632] ~ 'quinn-proto'
  AND status IN ('In Progress', 'Code Review') AND key != TC-8020
```

Fields requested: `summary, status, labels, assignee`

### Result (as provided by the eval scenario)

1 issue returned.

## Concurrent triage warning presented to the engineer

```
⚠️ Concurrent triage detected on the same upstream component (quinn-proto):

| CVE Issue | Status      | Assignee               |
|-----------|-------------|------------------------|
| TC-8019   | In Progress | engineer-b@example.com |

Another engineer is actively triaging a related CVE. Creating remediation
tasks now may produce duplicates.

Options:
1. Wait — pause until the other triage completes, then re-run Step 4.3
   to detect any overlap
2. Skip — skip remediation task creation for this CVE
3. Proceed — create tasks anyway with a `concurrent-triage-overlap` label
   so the other engineer's Step 4.3 catches the overlap
```

## Why this matters for TC-8020

- TC-8020 is affected in 2.2.x (2.2.0, 2.2.1, 2.2.2) and, cross-stream, in
  2.1.x (2.1.0, 2.1.1). Without intervention, Step 8 would create Cargo
  remediation tasks (2 per stream) that bump quinn-proto in `backend`.
- TC-8019 tracks a different CVE on the same crate (quinn-proto) and is actively
  In Progress under engineer-b@example.com. Its remediation would very likely
  bump the same crate in the same `Cargo.lock` on the same release branches
  (`release/0.4.z`, possibly `release/0.3.z`). Two independent sets of tasks
  would duplicate work and can conflict on the same branches.
- TC-8019 being assigned to a different user (not the current triager) confirms
  it is genuine concurrent triage, not our own earlier work.

## Handling of each option

| Choice | Action |
|--------|--------|
| **Wait** | Stop execution now. Tell the engineer to re-run triage of TC-8020 after TC-8019 completes; Step 4.3 (cross-CVE overlap) will then detect whether TC-8019's remediation (if its fix threshold is >= 0.11.14) already covers this CVE, and Step 7.5.3 dedup will link TC-8020 to the existing remediation Task instead of creating new ones. |
| **Skip** | Skip Step 8 entirely (no remediation tasks). Post a Jira comment on TC-8020 (with the triage-security Comment Footnote) explaining that task creation was skipped due to concurrent triage of TC-8019 on quinn-proto. |
| **Proceed** | Add label `concurrent-triage-overlap` to TC-8020 (after confirmation), then continue to Step 7.5 and Case A/B/C branching. The label lets TC-8019's Step 4.3 detect the overlap. |

## Gate status

**Blocked pending engineer decision.** Per the skill, execution does not continue
to Step 7.5 / Case A/B/C until the engineer chooses. No choice was supplied in this
eval, so no further Jira mutations (labels, comments, task creation) are performed.

**Recommendation:** Option 1 (**Wait**). TC-8019 is actively In Progress on the
same crate; waiting lets Step 4.3 / 7.5.3 reuse its remediation and avoids
duplicate tasks. Because the 2.2.x stream already ships the fix in 2.2.3+, waiting
carries low additional risk for current 2.2.x customers. If the past due date
(2026-07-15) makes waiting unacceptable, choose **Proceed** so the
`concurrent-triage-overlap` label flags the overlap. Coordinate directly with
engineer-b@example.com in either case.
