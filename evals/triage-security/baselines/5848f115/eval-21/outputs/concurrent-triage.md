# Step 7 -- Concurrent Triage Detection

## Prerequisites

The Upstream Affected Component custom field (`customfield_10632`) is configured in Security Configuration. The current issue TC-8020 has `customfield_10632` set to `quinn-proto`. This step is therefore active (not skipped).

## JQL Search

The following JQL query was executed to detect in-progress triages on the same upstream component:

```
project = TC
  AND issuetype = 10024
  AND cf[10632] ~ 'quinn-proto'
  AND status IN ('In Progress', 'Code Review')
  AND key != TC-8020
```

## Results

The search returned **one result**:

| CVE Issue | Status | Assignee |
|-----------|--------|----------|
| TC-8019 | In Progress | engineer-b@example.com |

## Analysis

Concurrent triage **is detected**. Another engineer (engineer-b@example.com) is actively triaging TC-8019, which targets the same upstream component (`quinn-proto`). TC-8019 is currently in "In Progress" status, meaning that engineer is likely in the middle of their own triage workflow and may be approaching or already at Step 8 (Remediation task creation).

Creating remediation tasks for TC-8020 now risks producing duplicate remediation tasks for the same library bump in the same stream, because:

1. Both TC-8019 and TC-8020 affect `quinn-proto`
2. TC-8019 is actively being triaged and may create remediation tasks that bump quinn-proto to >= 0.11.14
3. If both triages independently create upstream backport + downstream propagation tasks for the same stream, the result would be duplicate work

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

## Recommended Action

The recommended option depends on the engineer's judgment, but the key considerations are:

- **Wait** is the safest option: once TC-8019's triage completes, re-running Step 4.3 (cross-CVE overlap detection) will reveal whether TC-8019's remediation already covers TC-8020's fix threshold (quinn-proto >= 0.11.14). If it does, TC-8020 can be closed without creating duplicate tasks.
- **Skip** is appropriate if the engineer knows TC-8019 covers the same fix.
- **Proceed** is appropriate if urgency requires immediate action; the `concurrent-triage-overlap` label ensures that TC-8019's triage (via its own Step 4.3) will detect the overlap and handle deduplication.

No remediation tasks should be created until the engineer selects one of these three options.
