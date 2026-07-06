# Concurrent Triage Detection -- Step 7

## Prerequisite Check

The Upstream Affected Component custom field (`customfield_10632`) is configured in Security Configuration. The field on TC-8020 is set to `quinn-proto`. Step 7 proceeds.

## JQL Query

```
project = TC
  AND issuetype = 10024
  AND cf[10632] ~ 'quinn-proto'
  AND status IN ('In Progress', 'Code Review')
  AND key != TC-8020
```

## Results

The search returned **1 result**:

| CVE Issue | Status | Assignee |
|-----------|--------|----------|
| TC-8019 | In Progress | engineer-b@example.com |

## Warning Presented to Engineer

```
WARNING: Concurrent triage detected on the same upstream component (quinn-proto):

| CVE Issue | Status      | Assignee                |
|-----------|-------------|-------------------------|
| TC-8019   | In Progress | engineer-b@example.com  |

Another engineer is actively triaging a related CVE that affects quinn-proto.
Creating remediation tasks now may produce duplicates if the other triage's
remediation already bumps quinn-proto past this CVE's fix threshold (0.11.14).

Options:
1. Wait -- pause until TC-8019's triage completes, then re-run Step 4.3
   to detect any overlap from their remediation tasks
2. Skip -- skip remediation task creation for this CVE entirely
3. Proceed -- create tasks anyway with a `concurrent-triage-overlap` label
   so that TC-8019's Step 4.3 cross-CVE overlap detection catches the overlap
```

## Analysis

TC-8019 is actively being triaged by engineer-b@example.com and affects the same upstream component (`quinn-proto`). This creates a risk of duplicate remediation tasks:

- If TC-8019's triage creates a remediation task that bumps quinn-proto to >= 0.11.14, that task would also cover CVE-2026-31812 (TC-8020's vulnerability). Creating a second set of remediation tasks from TC-8020 would be redundant.
- If TC-8019's remediation bumps quinn-proto to a version below 0.11.14, the remediations are independent and both are needed.

Since TC-8019 is still In Progress (not yet at Step 8 remediation), the outcome is uncertain.

## Timing in the Workflow

This concurrent triage check runs at Step 7, which is **before** the Case A/B/C branching in Step 8. The engineer must choose one of the three options before the skill proceeds to determine whether to create remediation tasks (Case A), post cross-stream notices (Case B), or close as not affected (Case C).

## Recommended Action

The three options each serve a different scenario:

1. **Wait** is safest if TC-8019 is close to completing triage. After TC-8019 finishes and creates its remediation tasks, re-running triage on TC-8020 would allow Step 4.3 (cross-CVE overlap detection) to detect whether TC-8019's remediation already covers this CVE.

2. **Skip** is appropriate if the engineer has confirmed externally that TC-8019's remediation will cover this CVE's fix threshold.

3. **Proceed with `concurrent-triage-overlap` label** is appropriate if remediation is urgent (due date 2026-07-15) and the engineer wants to create tasks immediately, accepting possible duplication. The label ensures that when TC-8019's triage runs Step 4.3, it will detect the overlap and the duplicate can be reconciled.
