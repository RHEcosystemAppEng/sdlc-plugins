# Step 7 -- Concurrent Triage Detection: TC-8020

## Configuration

- **Upstream Affected Component custom field**: customfield_10632 (configured in Security Configuration)
- **Component value on TC-8020**: quinn-proto

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

## Analysis

Concurrent triage detected on the same upstream component (quinn-proto).

TC-8019 is currently **In Progress**, meaning another engineer (engineer-b@example.com) is actively triaging a different CVE that also affects the quinn-proto component. If both triages reach Step 8 (Remediation) simultaneously, they may create duplicate remediation tasks that bump quinn-proto on the same branches.

## Warning Presented to Engineer

```
Warning: Concurrent triage detected on the same upstream component (quinn-proto):

| CVE Issue | Status      | Assignee                 |
|-----------|-------------|--------------------------|
| TC-8019   | In Progress | engineer-b@example.com   |

Another engineer is actively triaging a related CVE. Creating remediation
tasks now may produce duplicates.

Options:
1. Wait -- pause until the other triage completes, then re-run Step 4.3
   to detect any overlap
2. Skip -- skip remediation task creation for this CVE
3. Proceed -- create tasks anyway with a `concurrent-triage-overlap` label
   so the other engineer's Step 4.3 catches the overlap
```

## Recommendation

The engineer should choose one of the three options:

1. **Wait** (recommended if TC-8019 is near completion) -- pausing allows the other triage to finish first. Re-running will let Step 4.3 (cross-CVE overlap detection) identify whether TC-8019's remediation already covers the quinn-proto bump to >= 0.11.14, potentially making new remediation tasks unnecessary.

2. **Skip** -- appropriate if the engineer confirms with engineer-b@example.com that TC-8019 already covers the needed fix.

3. **Proceed** -- appropriate if the triages target different fix thresholds or different streams. The `concurrent-triage-overlap` label ensures the other engineer's triage picks up the overlap in their Step 4.3.

## Impact on Triage Flow

- If **Wait** is chosen: stop execution, inform the user to re-run after TC-8019's triage completes.
- If **Skip** is chosen: skip Step 8 entirely (no remediation tasks created); add a Jira comment explaining why task creation was skipped.
- If **Proceed** is chosen: add the `concurrent-triage-overlap` label to TC-8020 and continue to Case A/B/C branching in Step 8.

No remediation tasks should be created until the engineer makes a choice.
