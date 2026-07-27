# Step 7 -- Concurrent Triage Detection

## Prerequisite Check

The Upstream Affected Component custom field (`customfield_10632`) is configured in Security Configuration. The current issue TC-8020 has this field set to `quinn-proto`. Step 7 proceeds.

## JQL Query

Search for in-progress triages on the same upstream component:

```
project = TC
  AND issuetype = 10024
  AND cf[10632] ~ 'quinn-proto'
  AND status IN ('In Progress', 'Code Review')
  AND key != TC-8020
```

## Search Results

The JQL search returned **1 result**:

| CVE Issue | Status | Assignee |
|-----------|--------|----------|
| TC-8019 | In Progress | engineer-b@example.com |

## Concurrent Triage Warning

**WARNING**: Concurrent triage detected on the same upstream component (`quinn-proto`).

Another engineer (`engineer-b@example.com`) is actively triaging a related CVE (TC-8019) that affects the same upstream component. The issue TC-8019 is currently **In Progress**, indicating active triage work. Creating remediation tasks for TC-8020 now may produce duplicate remediation tasks that target the same library bump in the same repositories.

## Options Presented to Engineer

> **Concurrent triage detected on the same upstream component (quinn-proto):**
>
> | CVE Issue | Status | Assignee |
> |-----------|--------|----------|
> | TC-8019 | In Progress | engineer-b@example.com |
>
> Another engineer is actively triaging a related CVE. Creating remediation
> tasks now may produce duplicates.
>
> **Options:**
> 1. **Wait** -- pause until the other triage completes, then re-run Step 4.3
>    to detect any overlap
> 2. **Skip** -- skip remediation task creation for this CVE
> 3. **Proceed** -- create tasks anyway with a `concurrent-triage-overlap` label
>    so the other engineer's Step 4.3 catches the overlap
>
> Choose (1/2/3):

## Option Details

- **Option 1 (Wait)**: Stop execution and inform the user to re-run triage after TC-8019's triage completes. At that point, Step 4.3 cross-CVE overlap detection will identify whether TC-8019's remediation already covers TC-8020's fix threshold, potentially avoiding duplicate task creation.

- **Option 2 (Skip)**: Skip Step 8 entirely -- do not create remediation tasks for TC-8020. A Jira comment would be posted explaining why task creation was skipped (concurrent triage on the same component). The rest of the triage (Affects Versions correction, labels, etc.) still applies.

- **Option 3 (Proceed)**: Add the `concurrent-triage-overlap` label to TC-8020 and continue to Case A/B/C branching in Step 8. The label ensures that when TC-8019's triage reaches Step 4.3, cross-CVE overlap detection picks up the overlap and avoids creating additional duplicate tasks.

## Timing

This concurrent triage check runs **before** Case A/B/C branching in Step 8. The user must choose one of the three options before remediation task creation (or closure) proceeds. No Jira mutations related to remediation tasks are performed until the user responds.
