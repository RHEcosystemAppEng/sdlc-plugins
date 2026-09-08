# Step 7 -- Concurrent Triage Detection for TC-8020

## Prerequisite Check

The Upstream Affected Component custom field (customfield_10632) is configured in Security Configuration. The current issue TC-8020 has this field set to **quinn-proto**. Proceeding with concurrent triage detection.

## JQL Search

Query executed (simulated):

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

A concurrent triage has been detected. TC-8019 is actively being triaged by engineer-b@example.com, and it targets the same upstream component (quinn-proto) as TC-8020. This means another engineer is currently working through triage steps for a different CVE that also affects the quinn-proto library.

Creating remediation tasks for TC-8020 now risks producing duplicate remediation tasks if TC-8019's triage also creates tasks to bump quinn-proto. Specifically:

- If TC-8019's remediation bumps quinn-proto to a version that meets or exceeds TC-8020's fix threshold (0.11.14), then TC-8020's remediation would be redundant.
- If TC-8019's remediation bumps quinn-proto to a lower version, then TC-8020 still needs its own remediation, but the two tasks would touch the same dependency in the same lock file, creating merge conflicts.

## Warning Presented to Engineer

```
WARNING: Concurrent triage detected on the same upstream component (quinn-proto):

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

**Option 1 (Wait)** is the safest choice. Once TC-8019's triage completes:
- Re-running Step 4.3 (Cross-CVE overlap detection) will detect whether TC-8019's remediation already covers TC-8020's fix threshold (quinn-proto >= 0.11.14).
- If the overlap is confirmed, TC-8020 can be closed without creating duplicate tasks.
- If there is no overlap (TC-8019 targets a different fix threshold), remediation tasks can be created without risk of duplication.

**Option 3 (Proceed)** is acceptable if time-sensitive. The `concurrent-triage-overlap` label ensures that when TC-8019's triage reaches its own Step 4.3 cross-CVE overlap detection, it will discover TC-8020's tasks and can reconcile any overlap at that point.

## Impact on Triage Flow

This gate fires before Case A/B/C branching in Step 8. The triage cannot proceed to remediation task creation until the engineer selects one of the three options. Steps 1-6 (data extraction, version impact analysis, Affects Versions correction, duplicate/sibling check, lifecycle check, already-fixed check) have all completed successfully prior to this gate.
