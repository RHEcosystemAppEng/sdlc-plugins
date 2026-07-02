# Step 7 -- Concurrent Triage Detection for TC-8020

## Prerequisite Check

The Upstream Affected Component custom field (`customfield_10632`) is configured in Security Configuration. The current issue TC-8020 has this field set to `quinn-proto`. Proceeding with concurrent triage detection.

## JQL Search

The following JQL query was executed to find in-progress triages on the same upstream component:

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

## Concurrent Triage Warning

**WARNING: Concurrent triage detected on the same upstream component (quinn-proto).**

Another engineer (engineer-b@example.com) is actively triaging TC-8019, which affects the same upstream component `quinn-proto`. TC-8019 is currently in "In Progress" status, meaning that engineer is between Step 1 (Data Extraction) and Step 8 (Remediation) of their own triage workflow.

Creating remediation tasks now may produce duplicate tasks if TC-8019's triage also reaches Step 8 and creates remediation for the same streams. Both triages target the same library in the same repositories, so their remediation tasks would overlap.

## Options Presented to Engineer

This warning is presented **before** Case A/B/C branching in Step 8. The engineer must choose one of the following options before triage can proceed to remediation:

1. **Wait** -- Pause this triage until TC-8019's triage completes. After TC-8019's triage is done, re-run from Step 4.3 (cross-CVE overlap detection) to check whether TC-8019's remediation already covers CVE-2026-31812's fix threshold (quinn-proto >= 0.11.14). This is the safest option to avoid duplicate remediation tasks.

2. **Skip** -- Skip remediation task creation for TC-8020 entirely. Do not create any remediation tasks in Step 8. A Jira comment will be added to TC-8020 explaining that task creation was skipped due to concurrent triage on the same upstream component (quinn-proto) by TC-8019. The triage analysis (version impact, Affects Versions correction) is preserved, but no Tasks are created.

3. **Proceed** -- Create remediation tasks anyway, but add a `concurrent-triage-overlap` label to TC-8020. This label ensures that when TC-8019's triage reaches Step 4.3 (cross-CVE overlap detection), it will detect TC-8020's remediation tasks and handle the overlap appropriately (either by linking to the existing tasks or closing as covered). This option is appropriate when the engineer is confident the two CVEs have different fix thresholds or when time pressure requires immediate action.

## Timing in Workflow

This concurrent triage detection (Step 7) runs **after** Steps 3-6 (Affects Versions correction, duplicate/sibling check, lifecycle check, already-fixed check) and **before** Step 8's Case A/B/C branching. The version impact analysis, Affects Versions correction, and duplicate checks are all complete at this point. Only the remediation task creation decision is gated by this step.

## Recommendation

Given that TC-8019 is actively in progress on the same component, **Option 1 (Wait)** is recommended unless there is urgency driven by the due date (2026-07-15). Waiting allows TC-8019's remediation to complete first, after which Step 4.3's cross-CVE overlap detection can determine whether the existing remediation already covers CVE-2026-31812's fix threshold of quinn-proto 0.11.14.
