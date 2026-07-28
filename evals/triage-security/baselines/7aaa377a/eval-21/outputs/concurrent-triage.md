# Step 7 -- Concurrent Triage Detection

## Context

Step 7 runs **before** Case A/B/C branching in Step 8. Its purpose is to check whether another engineer is actively triaging a different CVE that affects the same upstream component. This prevents duplicate remediation tasks when two concurrent triages reach Step 8 simultaneously.

## Prerequisite Check

- **Upstream Affected Component custom field**: Configured (customfield_10632)
- **Component value on TC-8020**: `quinn-proto`
- Prerequisite met -- proceeding with concurrent triage detection.

## JQL Search

The following JQL query was constructed to search for in-progress triages on the same upstream component:

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

```
WARNING: Concurrent triage detected on the same upstream component (quinn-proto):

| CVE Issue | Status      | Assignee                |
|-----------|-------------|-------------------------|
| TC-8019   | In Progress | engineer-b@example.com  |

Another engineer is actively triaging a related CVE for the same
upstream component (quinn-proto). Creating remediation tasks now
may produce duplicate remediation tasks if both triages create
tasks for the same library bump.

Options:
1. Wait -- pause until the other triage (TC-8019) completes,
   then re-run Step 4.3 to detect any overlap before creating
   remediation tasks
2. Skip -- skip remediation task creation for this CVE (TC-8020)
   entirely and add a Jira comment explaining why task creation
   was skipped
3. Proceed -- create remediation tasks anyway with a
   'concurrent-triage-overlap' label so the other engineer's
   Step 4.3 cross-CVE overlap detection catches the overlap

Choose (1/2/3):
```

## Analysis

- **TC-8019** is currently **In Progress**, meaning an engineer (engineer-b@example.com) is actively triaging a different CVE that also affects the **quinn-proto** library.
- If TC-8020 proceeds to create remediation tasks (Step 8, Case B), the upstream backport task would bump `quinn-proto` in the source repository. If TC-8019's triage also creates a task to bump `quinn-proto`, there would be duplicate remediation tasks targeting the same library.
- The three options allow the engineer to choose the safest path based on their knowledge of the concurrent triage's progress.

## User Decision Required

Step 8 (Case A/B/C branching) is **blocked** until the user selects one of the three options above. No remediation tasks, cross-stream analysis, or close recommendations are generated until the concurrent triage conflict is resolved.

### Option Outcomes

- **If Wait**: Execution stops. The user should re-run triage after TC-8019's triage completes. At that point, Step 4.3 (cross-CVE overlap detection) would detect whether TC-8019's remediation already covers this CVE's fix threshold.
- **If Skip**: Step 8 is skipped entirely. A Jira comment is posted on TC-8020 documenting that remediation task creation was skipped due to concurrent triage of TC-8019 on the same upstream component.
- **If Proceed**: The `concurrent-triage-overlap` label is added to TC-8020, and triage continues to Case A/B/C branching. The label ensures that when TC-8019's triage reaches Step 4.3, the cross-CVE overlap detection will identify TC-8020's remediation tasks and assess coverage.
