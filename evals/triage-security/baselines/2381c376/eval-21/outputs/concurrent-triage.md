# Step 7 -- Concurrent Triage Detection for TC-8020

## Prerequisite Check

The Upstream Affected Component custom field (`customfield_10632`) is configured in Security Configuration. The field value on TC-8020 is `quinn-proto`. This step proceeds (not skipped).

## JQL Search

The following JQL query was simulated to detect in-progress triages on the same upstream component:

```
project = TC
  AND issuetype = 10024
  AND cf[10632] ~ 'quinn-proto'
  AND status IN ('In Progress', 'Code Review')
  AND key != TC-8020
```

## Search Results

The query returned **1 result**:

| CVE Issue | Status | Assignee |
|-----------|--------|----------|
| TC-8019 | In Progress | engineer-b@example.com |

## Analysis

A concurrent triage has been detected. TC-8019 is actively being triaged by `engineer-b@example.com` and targets the same upstream component (`quinn-proto`). This means another engineer is already working on a different CVE that affects the same library. If both triages reach Step 8 (Remediation) simultaneously, they could create duplicate remediation tasks that both bump `quinn-proto` to a fixed version.

### Risk Assessment

- **Duplicate remediation tasks**: Both TC-8020 and TC-8019 may produce remediation tasks that bump `quinn-proto`. If TC-8019's remediation bumps `quinn-proto` to a version that also satisfies TC-8020's fix threshold (>= 0.11.14), then TC-8020's remediation tasks would be redundant.
- **Cross-CVE overlap**: Step 4.3 (Cross-CVE Overlap Detection) would normally detect if TC-8019's remediation already covers this CVE's fix threshold. However, since TC-8019 is still in progress, its remediation tasks may not yet exist or may not yet be linked.

### Options Presented to Engineer

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

### Recommended Action

**Option 1 (Wait)** is recommended when the other triage is expected to complete soon, as it avoids duplicate work. After TC-8019's triage completes, re-running Step 4.3 would detect any cross-CVE overlap and either link TC-8020 to an existing covering remediation task or confirm that new tasks are needed.

**Option 3 (Proceed)** is appropriate if the triage cannot be delayed (e.g., approaching the due date of 2026-07-15). The `concurrent-triage-overlap` label ensures that when TC-8019's triage runs its own Step 4.3, it will detect the overlap and avoid creating duplicate tasks on its side.

### Outcome

Triage execution pauses at Step 7 until the engineer selects one of the three options. No remediation tasks or further Jira mutations are performed until a choice is made.

### Proposed Jira Actions (if Option 3 -- Proceed is chosen)

- **Add label**: `concurrent-triage-overlap` to TC-8020
  - Proposed: `jira.edit_issue(TC-8020, fields={"labels": ["CVE-2026-31812", "pscomponent:org/rhtpa-server", "concurrent-triage-overlap"]})`
- Continue to Case A/B/C branching in Step 8
