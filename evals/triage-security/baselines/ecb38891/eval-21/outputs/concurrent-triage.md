# Step 7 -- Concurrent Triage Detection

This step runs **before** Case A/B/C branching in Step 8 to prevent duplicate remediation tasks when two concurrent triages target the same upstream component.

## Prerequisites

- Upstream Affected Component custom field (customfield_10632) is configured in Security Configuration.
- The current issue TC-8020 has customfield_10632 set to `quinn-proto`.

## JQL Search for In-Progress Triages

The following JQL query searches for other Vulnerability issues actively being triaged on the same upstream component:

```
project = TC AND issuetype = 10024 AND cf[10632] ~ 'quinn-proto' AND status IN ('In Progress', 'Code Review') AND key != TC-8020
```

## Search Results

The JQL search returned **one result**:

| CVE Issue | Status | Assignee |
|-----------|--------|----------|
| TC-8019 | In Progress | engineer-b@example.com |

## Concurrent Triage Warning

A concurrent triage was detected on the same upstream component (`quinn-proto`):

> **Concurrent triage detected** on the same upstream component (quinn-proto):
>
> | CVE Issue | Status | Assignee |
> |-----------|--------|----------|
> | TC-8019 | In Progress | engineer-b@example.com |
>
> Another engineer is actively triaging a related CVE. Creating remediation
> tasks now may produce duplicates.
>
> Options:
> 1. **Wait** -- pause until the other triage completes, then re-run Step 4.3 to detect any overlap
> 2. **Skip** -- skip remediation task creation for this CVE
> 3. **Proceed** -- create tasks anyway with a `concurrent-triage-overlap` label so the other engineer's Step 4.3 catches the overlap

## User Action Required

The triage is paused at Step 7, awaiting the engineer's choice before proceeding to Case A/B/C branching in Step 8.

### Option details

- **Wait**: Stop execution. The user should re-run triage after TC-8019's triage completes. At that point, Step 4.3 (cross-CVE overlap detection) will detect any overlap with TC-8019's remediation tasks.
- **Skip**: Skip Step 8 entirely (no remediation tasks are created). A Jira comment will be added to TC-8020 explaining why task creation was skipped due to concurrent triage on the same upstream component.
- **Proceed**: Add the `concurrent-triage-overlap` label to TC-8020 and continue to Case A/B/C branching. The label ensures the other triage's Step 4.3 cross-CVE overlap detection picks up the overlap when it reaches that step.
