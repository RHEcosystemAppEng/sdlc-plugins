# Step 7 -- Concurrent Triage Detection

## Overview

Before proceeding to Case A/B/C branching in Step 8, Step 7 checks whether another engineer is actively triaging a different CVE that affects the same upstream component. This prevents duplicate remediation tasks when two concurrent triages reach Step 8 simultaneously.

## Configuration Check

The Upstream Affected Component custom field is configured in Security Configuration. The current issue (TC-8020) has `customfield_10632` set to `quinn-proto`. Step 7 proceeds.

## JQL Search

The following JQL query was constructed to detect concurrent triages on the same upstream component:

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

**Concurrent triage detected on the same upstream component (quinn-proto):**

Another engineer (engineer-b@example.com) is actively triaging TC-8019, which also targets the upstream component `quinn-proto`. TC-8019 is currently **In Progress**, meaning that engineer may be in the process of creating remediation tasks for quinn-proto. Creating remediation tasks for TC-8020 now may produce duplicates if TC-8019's remediation already bumps quinn-proto past the fix threshold for CVE-2026-31812.

## Proposed Options

The following three options are presented to the engineer for decision:

1. **Wait** -- Pause triage of TC-8020 until TC-8019's triage completes. Once TC-8019 finishes, re-run from Step 4.3 to detect whether TC-8019's remediation task already covers CVE-2026-31812's fix threshold (quinn-proto >= 0.11.14). This is the safest option to avoid duplicate tasks.

2. **Skip** -- Skip remediation task creation for TC-8020 entirely. A Jira comment will be added to TC-8020 explaining that task creation was deferred due to concurrent triage of TC-8019 on the same upstream component. The rest of the triage (Affects Versions correction, labels, etc.) will still be applied.

3. **Proceed** -- Create remediation tasks for TC-8020 anyway, but add the `concurrent-triage-overlap` label to TC-8020. This label ensures that when TC-8019's triage reaches Step 4.3 (Cross-CVE Overlap Detection), it will detect the overlap and either reconcile or flag the duplicate remediation for manual resolution.

## Timing

This concurrent triage check runs **before** Case A/B/C branching in Step 8. No remediation tasks are created until the engineer selects one of the three options above. The triage flow is paused at this gate pending engineer input.
