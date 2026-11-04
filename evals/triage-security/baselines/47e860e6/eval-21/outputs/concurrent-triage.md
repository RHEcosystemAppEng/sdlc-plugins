# Step 7 – Concurrent Triage Detection: TC-8020

## Prerequisite check

- Upstream Affected Component custom field: **customfield_10632, configured** (eval assumption), so Step 7 runs.
- Field value on TC-8020: **quinn-proto**, which is non-empty, so the step proceeds.
- Step 7 needs only this field. PS Component and Stream fields are not required here. Those two are missing, which is why Step 4.3 cross-CVE overlap detection was skipped.

## JQL search (simulated, not executed)

```
project = TC AND issuetype = 10024
  AND cf[10632] ~ 'quinn-proto'
  AND status IN ('In Progress', 'Code Review')
  AND key != TC-8020
fields: summary, status, labels, assignee
```

## Result (simulated)

One concurrent triage was found:

| CVE Issue | Status | Assignee |
|-----------|--------|----------|
| TC-8019 | In Progress | engineer-b@example.com |

## Warning presented to the engineer

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

- TC-8019 tracks a different CVE on the same crate (quinn-proto). Its remediation will probably bump quinn-proto on the same release lines (release/0.4.z, possibly release/0.3.z). If it bumps to 0.11.14 or later, it also fixes CVE-2026-31812.
- Two independent triages reaching Step 8 at the same time would create duplicate "bump quinn-proto" upstream and downstream Tasks for the same stream.
- Step 4.3 could not catch this overlap automatically, for two reasons:
  - PS Component and Stream fields are not configured, so Step 4.3 was skipped.
  - TC-8019 is still in progress, so it may not have any linked remediation Task yet.

## Handling of each choice

| Choice | Action |
|--------|--------|
| Wait | Stop execution. Tell the user to re-run triage of TC-8020 after TC-8019 completes, then re-check overlap (Step 4.3, or a manual check of TC-8019's Depend-linked tasks and their bump version against 0.11.14). |
| Skip | Skip Step 8 (no remediation tasks). Post a Jira comment on TC-8020 explaining that task creation was skipped because of concurrent triage TC-8019 by engineer-b@example.com. The comment includes the triage-security Comment Footnote. |
| Proceed | Add label `concurrent-triage-overlap` to TC-8020 (needs confirmation), then continue to Step 7.5 and Case A/B. |

## Status

**Execution pauses at Step 7 until the engineer chooses.** The skill must not continue to Step 7.5 or Step 8 on its own. No Jira mutation was performed.

Recommended choice: **Wait** (or coordinate directly with engineer-b@example.com). In 2.2.x, the latest releases (2.2.3 and 2.2.4) already ship quinn-proto 0.11.14, so there is little urgency to create tasks right now. Waiting avoids duplicate tasks and lets the overlap be confirmed against TC-8019's remediation.
