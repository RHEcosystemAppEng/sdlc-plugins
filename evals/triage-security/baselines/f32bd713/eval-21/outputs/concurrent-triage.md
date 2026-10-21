# Step 7 -- Concurrent Triage Detection for TC-8020

## Prerequisites

- **Upstream Affected Component custom field**: Configured as `customfield_10632`
- **Upstream Affected Component value on TC-8020**: `quinn-proto`
- **Step 7 prerequisite met**: Yes -- the custom field is configured and populated

## JQL Search Executed

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

## Analysis

A concurrent triage has been detected. Another engineer (`engineer-b@example.com`) is actively triaging issue **TC-8019**, which affects the same upstream component (`quinn-proto`). TC-8019 is currently **In Progress**, meaning the engineer is actively working on it.

This creates a risk of duplicate remediation tasks: if both TC-8020 and TC-8019 reach Step 8 (Remediation) simultaneously, each triage could independently create remediation tasks that bump `quinn-proto` -- resulting in two sets of overlapping tasks for the same library fix.

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

## Option Analysis

### Option 1: Wait
- **Best when**: The concurrent triage (TC-8019) is nearly complete. Waiting ensures that when TC-8020's triage resumes, Step 4.3 (Cross-CVE Overlap Detection) will identify any remediation tasks already created by TC-8019's triage and avoid duplication.
- **Outcome**: Execution pauses. The engineer re-runs triage after TC-8019 completes.

### Option 2: Skip
- **Best when**: The engineer determines that TC-8019's remediation will fully cover the quinn-proto fix for the relevant streams, making TC-8020's remediation tasks unnecessary.
- **Outcome**: Step 8 is skipped entirely. A Jira comment is posted on TC-8020 explaining that remediation task creation was skipped due to concurrent triage on the same component (TC-8019).

### Option 3: Proceed
- **Best when**: The engineer determines that TC-8019 and TC-8020 may require different remediation (e.g., different CVEs with different fix thresholds), or that coordination is easier post-creation.
- **Outcome**: Remediation tasks are created with the `concurrent-triage-overlap` label added to TC-8020. This label ensures that when TC-8019's engineer runs their Step 4.3 (Cross-CVE Overlap Detection), the overlap between the two triages will be detected and reconciled.

## Recommendation

Given that TC-8019 is actively In Progress on the same upstream component (`quinn-proto`), the **recommended option is Option 1 (Wait)** unless the engineer has specific knowledge that the two CVEs require independent remediation. Waiting allows the first triage to complete its remediation task creation, after which TC-8020's re-run will detect the overlap via Step 4.3 and either reuse existing remediation tasks or create only the necessary additional ones.

If the engineer chooses Option 3 (Proceed), the `concurrent-triage-overlap` label will be added to TC-8020 before continuing to Case A/B/C branching in Step 8.
