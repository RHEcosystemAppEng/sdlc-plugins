# Step 7 -- Concurrent Triage Detection for TC-8020

## Prerequisite Check

The Upstream Affected Component custom field (`customfield_10632`) is configured in Security Configuration. The current issue TC-8020 has `customfield_10632` set to `quinn-proto`. This field is populated, so concurrent triage detection proceeds.

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

**Concurrent triage detected on the same upstream component (quinn-proto).**

Another engineer (`engineer-b@example.com`) is actively triaging TC-8019, which also affects the `quinn-proto` upstream component. TC-8019 is currently in `In Progress` status, meaning its triage is underway and may be approaching or already past its own Step 8 (remediation task creation).

Creating remediation tasks for TC-8020 now could produce duplicates if TC-8019's triage also creates remediation tasks that bump `quinn-proto` to >= 0.11.14 for the same streams.

## Options Presented to Engineer

1. **Wait** -- Pause triage until TC-8019's triage completes. After it completes, re-run from Step 4.3 (cross-CVE overlap detection) to check whether TC-8019's remediation tasks already cover TC-8020's fix threshold (quinn-proto >= 0.11.14). This is the safest option to avoid duplicate work.

2. **Skip** -- Skip remediation task creation (Step 8) entirely for TC-8020. Add a Jira comment explaining that task creation was skipped due to concurrent triage on the same component. The triage analysis (Steps 1-6) is preserved; only task creation is deferred.

3. **Proceed** -- Create remediation tasks anyway with a `concurrent-triage-overlap` label added to TC-8020. This label ensures that when TC-8019's triage runs its Step 4.3 (cross-CVE overlap detection), it will discover TC-8020's tasks and can reconcile any overlap. This is appropriate when the two CVEs require different fix thresholds or when the engineer is confident there will be no overlap.

## Risk Assessment

Since both TC-8019 and TC-8020 affect the same upstream component (`quinn-proto`), there is a meaningful risk of duplicate remediation tasks if both triages create tasks targeting the same streams (especially 2.1.x and 2.2.x). The concurrent triage detection mechanism exists specifically to surface this risk before task creation.

The recommended approach depends on the relationship between TC-8019 and TC-8020:
- If TC-8019 is for a **different CVE** that also requires bumping quinn-proto, the remediation tasks may overlap -- **Wait** is recommended.
- If TC-8019 is for the **same CVE** (a sibling issue for a different stream), Step 4 (duplicate/sibling detection) would have already handled the relationship -- **Proceed** is likely safe.
- If the engineer has context about TC-8019's scope, they can make an informed choice among the three options.

## Decision Required

The engineer must choose one of the three options before triage can proceed to Case A/B/C remediation branching. Triage Steps 1-6 (data extraction, version impact analysis, Affects Versions correction, duplicate/sibling check, lifecycle check, already-fixed check) are complete. Only Step 8 (remediation task creation) is gated by this concurrent triage detection.
