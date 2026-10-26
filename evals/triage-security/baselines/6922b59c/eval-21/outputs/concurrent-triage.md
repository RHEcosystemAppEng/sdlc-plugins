# Step 7 -- Concurrent Triage Detection for TC-8020

## Prerequisite Check

- Upstream Affected Component custom field: **configured** (customfield_10632)
- Upstream Affected Component value on TC-8020: **quinn-proto**
- Prerequisite met: proceed with concurrent triage detection

## JQL Search

Query executed (simulated):

```
project = TC
  AND issuetype = 10024
  AND cf[10632] ~ 'quinn-proto'
  AND status IN ('In Progress', 'Code Review')
  AND key != TC-8020
```

## Results

The JQL search returned **1 result**:

| CVE Issue | Status | Assignee |
|-----------|--------|----------|
| TC-8019 | In Progress | engineer-b@example.com |

## Analysis

Concurrent triage **detected** on the same upstream component (`quinn-proto`).

Another engineer (engineer-b@example.com) is actively triaging TC-8019, a different CVE Vulnerability issue that also affects the quinn-proto library. TC-8019 is currently in "In Progress" status, meaning that engineer is likely performing their own version impact analysis and may be about to create remediation tasks for the same upstream component.

### Risk

Creating remediation tasks for TC-8020 now may produce duplicates if TC-8019's triage also creates tasks that bump quinn-proto. Both triages would independently create upstream backport or dependency bump tasks targeting the same library in the same streams, resulting in redundant work.

### Warning Presented to Engineer

```
Concurrent triage detected on the same upstream component (quinn-proto):

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

### Options Explained

1. **Wait**: Halt triage of TC-8020. After TC-8019's triage completes and its remediation tasks are created, re-run this triage. At that point, Step 4.3 (Cross-CVE Overlap Detection) will detect whether TC-8019's remediation tasks already cover TC-8020's fix threshold (quinn-proto >= 0.11.14). If they do, TC-8020 can be closed without creating new tasks.

2. **Skip**: Skip remediation task creation entirely for TC-8020. A Jira comment is added to TC-8020 explaining that task creation was skipped due to concurrent triage on TC-8019. The engineer can revisit after TC-8019 completes.

3. **Proceed**: Continue with remediation task creation for TC-8020 but add the `concurrent-triage-overlap` label. This label ensures that when TC-8019's triage reaches its own Step 4.3, the cross-CVE overlap detection will find TC-8020's remediation tasks and can reconcile duplicates. This is the safest option if TC-8020's due date (2026-07-15) is approaching and waiting is not feasible.

### Recommendation

Given that:
- TC-8019 is already "In Progress" (likely nearing completion)
- Both CVEs target the same library (quinn-proto)
- The fix threshold for TC-8020 is 0.11.14

**Option 1 (Wait)** is recommended if timeline permits. TC-8019's remediation may already bump quinn-proto to or past 0.11.14, which would make TC-8020's remediation redundant. Waiting avoids duplicate task creation entirely.

If the due date is urgent, **Option 3 (Proceed)** with the `concurrent-triage-overlap` label is the fallback -- Step 4.3's cross-CVE overlap mechanism will reconcile any duplicates after both triages complete.

The engineer must choose before triage can proceed to Case A/B/C branching and remediation task creation (Step 8).
