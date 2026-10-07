# Step 7 -- Concurrent Triage Detection for TC-8020

## Prerequisite Check

- Upstream Affected Component custom field: **configured** (customfield_10632)
- Upstream Affected Component value on TC-8020: **quinn-proto**
- Field is populated: **yes**
- Prerequisite met: **yes** -- proceed with concurrent triage detection.

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

The JQL search returned **1 result**:

| CVE Issue | Status | Assignee |
|-----------|--------|----------|
| TC-8019 | In Progress | engineer-b@example.com |

## Analysis

Concurrent triage **detected** on the same upstream component (`quinn-proto`).

TC-8019 is currently In Progress, meaning another engineer (engineer-b@example.com)
is actively triaging a different CVE that also affects the quinn-proto component.
If both triages proceed to Step 8 (Remediation) independently, they may create
duplicate remediation tasks targeting the same library bump in the same repositories.

## Warning Presented to Engineer

```
!! Concurrent triage detected on the same upstream component (quinn-proto):

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
- Stop execution and inform the user to re-run after TC-8019's triage completes.
- Safest approach: ensures no duplicate remediation tasks are created.
- After TC-8019's triage completes, re-running TC-8020's triage from Step 4.3
  will detect any overlap from TC-8019's remediation tasks and avoid duplication.

### Option 2: Skip
- Skip Step 8 entirely (do not create remediation tasks).
- Add a Jira comment to TC-8020 explaining why task creation was skipped.
- Appropriate when TC-8019's remediation is expected to cover the same fix threshold.

### Option 3: Proceed
- Add the `concurrent-triage-overlap` label to TC-8020.
- Continue to Case A/B/C branching and create remediation tasks.
- The `concurrent-triage-overlap` label ensures TC-8019's Step 4.3 cross-CVE
  overlap detection picks up the overlap when that triage reaches its own
  remediation step.
- Use this when the CVEs require different fix thresholds or the engineer
  determines the overlap risk is acceptable.

## Recommendation

Given that TC-8019 is actively being triaged on the same component (quinn-proto),
**Option 1 (Wait)** is the safest approach to avoid duplicate remediation tasks.
However, the final decision rests with the engineer. If the engineer knows that
TC-8019 targets a different fix threshold or different streams, Option 3 (Proceed
with label) may be appropriate.

The triage cannot proceed past this point until the engineer selects an option.
