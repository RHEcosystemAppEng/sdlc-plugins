# Step 7 -- Concurrent Triage Detection

## Configuration

The Upstream Affected Component custom field (`customfield_10632`) is configured in Security Configuration. The current issue TC-8020 has this field set to `quinn-proto`.

## JQL Query

The following JQL query was executed to detect concurrent triages on the same upstream component:

```
project = TC
  AND issuetype = 10024
  AND cf[10632] ~ 'quinn-proto'
  AND status IN ('In Progress', 'Code Review')
  AND key != TC-8020
```

## Results

The query returned **1 result**:

| CVE Issue | Status | Assignee |
|-----------|--------|----------|
| TC-8019 | In Progress | engineer-b@example.com |

## Analysis

A concurrent triage has been detected. Another engineer (`engineer-b@example.com`) is actively triaging TC-8019, which affects the same upstream component (`quinn-proto`). TC-8019 is currently `In Progress`, meaning that engineer is likely working through the same triage steps and may reach Step 8 (Remediation) around the same time as this triage of TC-8020.

### Risk

If both triages proceed to create remediation tasks independently, duplicate tasks could be created for the same library bump (quinn-proto to >= 0.11.14) on the same streams. This would result in:

- Duplicate upstream backport tasks (bumping quinn-proto in the same source repo branch)
- Duplicate downstream propagation tasks (updating the same Konflux release repo reference)
- Wasted engineering effort and potential merge conflicts

### Warning Presented

```
Warning: Concurrent triage detected on the same upstream component (quinn-proto):

| CVE Issue | Status      | Assignee                  |
|-----------|-------------|---------------------------|
| TC-8019   | In Progress | engineer-b@example.com    |

Another engineer is actively triaging a related CVE that affects quinn-proto.
Creating remediation tasks now may produce duplicates.

Options:
1. Wait -- pause until the other triage completes, then re-run Step 4.3
   to detect any overlap
2. Skip -- skip remediation task creation for this CVE
3. Proceed -- create tasks anyway with a `concurrent-triage-overlap` label
   so the other engineer's Step 4.3 catches the overlap
```

### Recommended Action

**Option 1 (Wait)** is recommended in this case. Since TC-8019 is already `In Progress` and both CVEs affect the same component (`quinn-proto`), it is likely that TC-8019's remediation tasks will cover the fix needed for TC-8020 as well (both likely require bumping quinn-proto to >= 0.11.14). Waiting allows Step 4.3 (Cross-CVE overlap detection) to identify if TC-8019's remediation already covers TC-8020's fix threshold, potentially avoiding the need to create any new remediation tasks.

If the user chooses **Option 3 (Proceed)**, the `concurrent-triage-overlap` label would be added to TC-8020, and remediation tasks would be created. The other engineer's triage of TC-8019 would then detect the overlap in their Step 4.3 and handle deduplication.

If the user chooses **Option 2 (Skip)**, Step 8 is skipped entirely, and a Jira comment would be posted on TC-8020 explaining that remediation task creation was skipped due to the concurrent triage on TC-8019.

## Outcome

Execution pauses at Step 7 until the user selects one of the three options. No remediation tasks (Case A/B/C) are created until the user responds.
