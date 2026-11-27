# Step 7 – Concurrent Triage Detection: TC-8020

## Prerequisite check

- Upstream Affected Component custom field: **configured** (`customfield_10632`, per task
  assumption) → step is NOT skipped.
- Current issue value of customfield_10632: **`quinn-proto`** (non-empty) → proceed.

## JQL search (simulated — no Jira call made)

```
project = TC AND issuetype = 10024 AND cf[10632] ~ 'quinn-proto'
  AND status IN ('In Progress', 'Code Review') AND key != TC-8020
fields: summary, status, labels, assignee
```

Simulated result: **1 issue**.

## Result presented to the engineer

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

## Analysis

- TC-8019 is a different Vulnerability issue on the same upstream component (quinn-proto),
  actively In Progress under another engineer (engineer-b@example.com), so it is a true
  concurrent triage, not this triager's own work.
- TC-8020 needs remediation in stream 2.2.x (2.2.0, 2.2.1, 2.2.2 ship quinn-proto < 0.11.14).
  If TC-8019 is also making a quinn-proto bump for 2.2.x, both triages could create
  duplicate upstream-bump / downstream-propagation tasks for the same crate and stream.
- Step 4.3 (cross-CVE overlap) only catches remediation tasks that **already exist**; an
  in-flight triage has no tasks yet, which is exactly the gap Step 7 covers.

## Handling per option

| Choice | Action |
|---|---|
| Wait | Stop execution now. Tell the engineer to re-run triage of TC-8020 after TC-8019 finishes; Step 4.3 will then detect whether TC-8019's remediation bumps quinn-proto to >= 0.11.14 for 2.2.x. |
| Skip | Skip Step 8 (no remediation tasks). Post a Jira comment on TC-8020 (with Comment Footnote) explaining that task creation was skipped because of concurrent triage TC-8019 on quinn-proto. |
| Proceed | Add label `concurrent-triage-overlap` to TC-8020, then continue to Step 7.5 and Case A/B/C. The label lets TC-8019's Step 4.3 detect the overlap. |

## Gate status

**Blocked pending engineer decision.** The skill requires an explicit user choice before
continuing to Step 7.5 / Case A/B/C. No choice was given in this eval, so no option is
assumed and no Jira mutation (label, comment, or task) is performed.
