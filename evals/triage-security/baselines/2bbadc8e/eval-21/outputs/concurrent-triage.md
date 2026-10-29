# Step 7 -- Concurrent Triage Detection for TC-8020

## Prerequisite Check

The Upstream Affected Component custom field (customfield_10632) IS configured in Security Configuration. The field on TC-8020 is set to `quinn-proto`. This step proceeds (not skipped).

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

## Analysis

**Concurrent triage detected.** Another engineer (engineer-b@example.com) is actively triaging TC-8019, which affects the same upstream component (`quinn-proto`). TC-8019 is currently In Progress, meaning that engineer is likely between Steps 1-8 of their own triage.

Creating remediation tasks for TC-8020 now risks producing **duplicate remediation tasks** if TC-8019's triage also reaches Step 8 and creates tasks for the same quinn-proto library bump. When both triages complete, the overlapping tasks would need to be reconciled via Step 4.3 (Cross-CVE overlap detection) or Step 7.5.3 (Cross-CVE dedup), but it is more efficient to avoid the duplication in the first place.

## PROPOSED Options for Engineer

Per the skill methodology, the following options would be presented to the engineer:

> **Concurrent triage detected on the same upstream component (quinn-proto):**
>
> | CVE Issue | Status | Assignee |
> |-----------|--------|----------|
> | TC-8019 | In Progress | engineer-b@example.com |
>
> Another engineer is actively triaging a related CVE. Creating remediation
> tasks now may produce duplicates.
>
> Options:
> 1. **Wait** -- pause until TC-8019's triage completes, then re-run Step 4.3
>    to detect any overlap
> 2. **Skip** -- skip remediation task creation for this CVE
> 3. **Proceed** -- create tasks anyway with a `concurrent-triage-overlap` label
>    so the other engineer's Step 4.3 catches the overlap

## Recommended Action

**Option 3 (Proceed with label)** is the recommended path for this triage. Rationale:

- TC-8020 and TC-8019 may address different CVEs that happen to affect the same upstream component. Each CVE needs its own triage record for audit purposes.
- The `concurrent-triage-overlap` label ensures that when TC-8019's triage reaches Step 4.3 (Cross-CVE overlap detection), it will find TC-8020's remediation tasks and can reconcile any duplicates.
- Waiting introduces delay and requires manual re-invocation, which may be forgotten.
- Skipping leaves TC-8020 without remediation tasks, creating a gap.

If the engineer selects Option 3, the PROPOSED Jira mutation would be:

**PROPOSAL: Add label `concurrent-triage-overlap` to TC-8020** (field-edit) before proceeding to Case A/B/C branching.
