# Step 7 -- Concurrent Triage Detection

## Prerequisite check

The Upstream Affected Component custom field (customfield_10632) is configured in Security Configuration. The current issue TC-8020 has customfield_10632 set to `quinn-proto`. Proceeding with concurrent triage detection.

## JQL search

The following JQL query would be executed to detect in-progress triages on the same upstream component:

```
project = TC
  AND issuetype = 10024
  AND cf[10632] ~ 'quinn-proto'
  AND status IN ('In Progress', 'Code Review')
  AND key != TC-8020
```

## Search results

The JQL search returned **1 result**:

| CVE Issue | Status | Assignee |
|-----------|--------|----------|
| TC-8019 | In Progress | engineer-b@example.com |

## Concurrent triage warning

**WARNING: Concurrent triage detected on the same upstream component (quinn-proto).**

Another engineer is actively triaging a related CVE that affects the same upstream component. TC-8019 is currently In Progress, assigned to engineer-b@example.com. Creating remediation tasks now may produce duplicate remediation work targeting the same library (quinn-proto) in the same source repository.

**Options:**

1. **Wait** -- Pause until the other triage (TC-8019) completes, then re-run Step 4.3 to detect any overlap from completed remediation tasks. This is the safest option to avoid duplicate work.
2. **Skip** -- Skip remediation task creation for this CVE entirely. A Jira comment will be added to TC-8020 explaining why task creation was skipped due to concurrent triage on the same component.
3. **Proceed** -- Create remediation tasks anyway with a `concurrent-triage-overlap` label added to TC-8020. This label ensures that the other triage's Step 4.3 cross-CVE overlap detection will pick up the overlap and can reconcile duplicate tasks.

## Timing

This concurrent triage check runs **before** Case A/B/C branching in Step 8. No remediation tasks, cross-stream impact comments, or close recommendations are generated until the engineer selects one of the three options above.

## Recommendation

Given that TC-8019 is actively being triaged by engineer-b@example.com for the same component (quinn-proto), the recommended approach is:

- **If the other triage is expected to complete soon**: choose **Option 1 (Wait)** to avoid potential duplicate remediation tasks.
- **If timing is urgent**: choose **Option 3 (Proceed)** with the `concurrent-triage-overlap` label so that overlap can be detected and reconciled later via Step 4.3.

Awaiting engineer decision before proceeding to Step 8.
