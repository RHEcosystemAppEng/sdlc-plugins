# Step 7 -- Concurrent Triage Detection for TC-8020

## Prerequisite Check

The Upstream Affected Component custom field (`customfield_10632`) is configured
in Security Configuration. The current issue TC-8020 has `customfield_10632`
set to `quinn-proto`. Proceeding with concurrent triage detection.

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

The search returned **1 result**:

| CVE Issue | Status | Assignee |
|-----------|--------|----------|
| TC-8019 | In Progress | engineer-b@example.com |

## Concurrent Triage Warning

Another engineer (`engineer-b@example.com`) is actively triaging TC-8019, which
affects the same upstream component (`quinn-proto`). TC-8019 is currently
`In Progress`, meaning that engineer is likely at or past Step 8 (remediation
task creation).

Creating remediation tasks for TC-8020 now may produce duplicate tasks that
target the same library bump (quinn-proto to >= 0.11.14) on the same upstream
branch and Konflux release repo.

## Risk Assessment

- **Component overlap**: Both TC-8020 and TC-8019 target the same upstream
  component (`quinn-proto`). If TC-8019's remediation task bumps quinn-proto
  to a version that also satisfies TC-8020's fix threshold (>= 0.11.14), the
  remediation for TC-8020 would be redundant.
- **Duplicate task risk**: If both triages create upstream backport tasks for
  the same branch (e.g., `release/0.4.z`), engineers would be assigned
  overlapping work.
- **Mitigation via Step 4.3**: If the engineer chooses to proceed, adding the
  `concurrent-triage-overlap` label ensures that TC-8019's Step 4.3 (cross-CVE
  overlap detection) will detect the overlap and link the issues appropriately.

## Options Presented to Engineer

```
Warning: Concurrent triage detected on the same upstream component (quinn-proto):

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

## Recommended Action

**Option 1 (Wait)** is the safest choice. Since TC-8019 is already `In Progress`,
its triage may complete soon. Once TC-8019's remediation tasks are created, re-running
triage on TC-8020 would allow Step 4.3 (cross-CVE overlap detection) to check whether
TC-8019's remediation already bumps quinn-proto past the fix threshold for
CVE-2026-31812 (>= 0.11.14). If so, TC-8020 can be closed as already covered
without creating duplicate tasks.

**Option 3 (Proceed)** is acceptable if the engineer wants to complete triage now.
The `concurrent-triage-overlap` label will ensure that the other engineer's triage
detects the overlap via Step 4.3, and any duplicate remediation can be reconciled
after the fact.

**Option 2 (Skip)** should be used only if the engineer determines that TC-8019's
remediation will definitively cover TC-8020's fix threshold and no separate tracking
is needed.
