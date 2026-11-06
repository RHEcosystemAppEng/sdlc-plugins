# Step 7 – Concurrent Triage Detection: TC-8020

## Prerequisite check

- Upstream Affected Component custom field: **configured** (customfield_10632, per eval assumption).
- Value on TC-8020: **quinn-proto** (non-empty) -> step runs (not skipped).

## Query (simulated)

```
jira.search_jql(
  "project = TC AND issuetype = 10024 AND cf[10632] ~ 'quinn-proto' AND status IN ('In Progress', 'Code Review') AND key != TC-8020",
  fields: ["summary", "status", "labels", "assignee"]
)
```

`10632` is the numeric portion of `customfield_10632`. The query was not actually executed; the eval-supplied result is used.

## Result

One result returned -> concurrent triage detected.

```
WARNING: Concurrent triage detected on the same upstream component (quinn-proto):

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

## Analysis

- TC-8019 is a *different* Vulnerability issue against the same upstream crate (quinn-proto), actively being worked by
  engineer-b@example.com. Its CVE ID, stream, and remediation plan are not in the returned fields, so we can't tell
  whether its remediation (a quinn-proto bump) would meet TC-8020's fix threshold of 0.11.14.
- TC-8020 itself needs quinn-proto >= 0.11.14 in stream 2.2.x (2.2.0, 2.2.1, 2.2.2 affected) and, cross-stream, in
  2.1.x (2.1.0, 2.1.1 affected). If TC-8019 is creating a quinn-proto bump task for the same streams, creating TC-8020
  tasks now would likely duplicate that work (e.g. two `release/0.3.z` quinn-proto bumps).
- Step 4.3 could not catch this overlap automatically: it was skipped because the PS Component and Stream custom fields
  are not configured. Also, TC-8019 is still in progress, so it has no completed remediation tasks to compare.

## Handling per choice

| Choice | Action |
|---|---|
| Wait | Stop execution; tell the engineer to re-run triage of TC-8020 after TC-8019 completes (then re-check overlap per Step 4.3). No Jira mutations. |
| Skip | Skip Step 8 (no remediation tasks); post a Jira comment on TC-8020 explaining task creation was skipped due to concurrent triage TC-8019 (with Comment Footnote). |
| Proceed | Add label `concurrent-triage-overlap` to TC-8020, then continue to Step 7.5 and Case A/B/C. |

## Recommendation

**Option 1 – Wait** (coordinate with engineer-b@example.com). Reasons:
- Duplicate remediation is likely for the same crate and the same Cargo.lock files.
- The 2.2.x stream already ships the fixed version (0.11.14) from 2.2.3 onward, and the Jira due date (2026-07-15) has
  already passed, so waiting a short while for TC-8019 adds little extra risk.
- The 2.1.x bump is the real outstanding work, and TC-8019 may already cover it.

Per the skill, execution does not continue to Step 7.5 / Case A/B/C until the engineer picks an option. In this
non-interactive eval no choice was given, so triage **halts at Step 7** awaiting the engineer's decision.
