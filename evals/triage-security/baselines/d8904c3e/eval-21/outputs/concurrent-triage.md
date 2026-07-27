# Step 7 -- Concurrent Triage Detection

## Prerequisite Check

The Upstream Affected Component custom field (`customfield_10632`) is configured in Security Configuration. The current issue TC-8020 has this field set to **quinn-proto**. Step 7 proceeds.

## JQL Search

The following JQL query was executed to find in-progress triages on the same upstream component:

```
project = TC
  AND issuetype = 10024
  AND cf[10632] ~ 'quinn-proto'
  AND status IN ('In Progress', 'Code Review')
  AND key != TC-8020
```

## Search Results

The search returned **1 result**:

| CVE Issue | Status | Assignee |
|-----------|--------|----------|
| TC-8019 | In Progress | engineer-b@example.com |

## Analysis

Concurrent triage detected on the same upstream component (quinn-proto). Another engineer (engineer-b@example.com) is actively triaging TC-8019, which also affects the quinn-proto component. Both triages may produce remediation tasks that bump quinn-proto, leading to duplicate tasks if both reach Step 8 independently.

## Warning Presented to Engineer

```
Concurrent triage detected on the same upstream component (quinn-proto):

| CVE Issue | Status      | Assignee                  |
|-----------|-------------|---------------------------|
| TC-8019   | In Progress | engineer-b@example.com    |

Another engineer is actively triaging a related CVE. Creating remediation
tasks now may produce duplicates.

Options:
1. Wait -- pause until the other triage completes, then re-run Step 4.3
   to detect any overlap
2. Skip -- skip remediation task creation for this CVE
3. Proceed -- create tasks anyway with a `concurrent-triage-overlap` label
   so the other engineer's Step 4.3 catches the overlap
```

## Rationale

The concurrent triage detection is significant because:

1. **TC-8019** is actively being triaged (status: In Progress) by another engineer for the same upstream component (quinn-proto).
2. If both triages independently create remediation tasks to bump quinn-proto, the team would end up with duplicate remediation work.
3. Depending on the fix thresholds of TC-8019's CVE versus TC-8020's CVE (CVE-2026-31812, fixed in 0.11.14), the remediation from TC-8019 may already cover TC-8020's fix threshold -- this would be detected by Step 4.3 (cross-CVE overlap detection) if the engineer chooses to wait.

## Recommended Action

The recommended option depends on coordination needs:

- **Option 1 (Wait)** is safest -- it prevents duplicate tasks entirely and allows Step 4.3 to detect if TC-8019's remediation already covers TC-8020.
- **Option 3 (Proceed)** is acceptable when timelines are tight -- the `concurrent-triage-overlap` label ensures the other engineer's Step 4.3 will catch the overlap and reconcile.
- **Option 2 (Skip)** should only be used if the engineer confirms through out-of-band coordination that TC-8019's remediation will cover TC-8020.

The engineer must choose before the triage can proceed to Case A/B/C branching in Step 8.
