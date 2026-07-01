# Step 7 -- Concurrent Triage Detection

## Upstream Affected Component

The Upstream Affected Component custom field (`customfield_10632`) is configured in Security Configuration and set to **quinn-proto** on the current issue TC-8020.

## JQL Query Executed

```
project = TC AND issuetype = 10024 AND cf[10632] ~ 'quinn-proto' AND status IN ('In Progress', 'Code Review') AND key != TC-8020
```

This query searches for other Vulnerability issues that:
- Are in the same project (TC)
- Are Vulnerability issue type (10024)
- Have the same Upstream Affected Component value (quinn-proto)
- Are currently being actively triaged (In Progress or Code Review status)
- Are not the current issue (TC-8020)

## Search Results

The JQL search returned **1 result**:

| CVE Issue | Status | Assignee |
|-----------|--------|----------|
| TC-8019 | In Progress | engineer-b@example.com |

## Concurrent Triage Warning

**Concurrent triage detected** on the same upstream component (quinn-proto):

TC-8019 is currently **In Progress** and assigned to **engineer-b@example.com**. Another engineer is actively triaging a related CVE that affects the same upstream library (quinn-proto). Creating remediation tasks now may produce duplicate tasks if both triages reach Step 8 simultaneously.

### Proposed Options

The following options are presented to the engineer for decision:

1. **Wait** -- Pause triage until TC-8019 completes its triage, then re-run Step 4.3 to detect any overlap from TC-8019's remediation tasks. This is the safest option to avoid duplicate work.

2. **Skip** -- Skip remediation task creation for TC-8020 entirely. A Jira comment will be posted explaining why task creation was skipped due to the concurrent triage on TC-8019.

3. **Proceed** -- Create remediation tasks anyway with a `concurrent-triage-overlap` label added to TC-8020. This label ensures that when TC-8019's triage runs Step 4.3 (cross-CVE overlap detection), it will detect the overlap and can reconcile the remediation tasks.

## Status

This check runs **before** Case A/B/C branching in Step 8. The triage flow is paused pending the engineer's selection from the three options above. No remediation tasks will be created until the engineer confirms their choice.
