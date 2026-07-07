# Step 7 -- Concurrent Triage Detection: TC-8020

## Configuration

The Upstream Affected Component custom field (`customfield_10632`) is configured in Security Configuration. This step is therefore **active** (not skipped).

## Current Issue Component

- **Issue**: TC-8020
- **Upstream Affected Component** (`customfield_10632`): `quinn-proto`

## JQL Search

The following JQL query was executed to detect in-progress triages on the same upstream component:

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

**WARNING: Concurrent triage detected on the same upstream component (quinn-proto).**

Another engineer (`engineer-b@example.com`) is actively triaging issue TC-8019, which affects the same upstream component `quinn-proto`. Both TC-8019 and TC-8020 target the same library, meaning their remediation tasks could overlap -- if both triages independently create remediation tasks that bump `quinn-proto`, the result would be duplicate tasks for the same dependency update.

This check runs **before** Case A/B/C branching in Step 8 to prevent duplicate remediation task creation when two concurrent triages reach Step 8 simultaneously.

## Options Presented to Engineer

```
WARNING: Concurrent triage detected on the same upstream component (quinn-proto):

| CVE Issue | Status      | Assignee                |
|-----------|-------------|-------------------------|
| TC-8019   | In Progress | engineer-b@example.com  |

Another engineer is actively triaging a related CVE. Creating remediation
tasks now may produce duplicates.

Options:
1. Wait -- pause until the other triage (TC-8019, assigned to
   engineer-b@example.com) completes, then re-run Step 4.3 to detect any
   overlap from their remediation tasks
2. Skip -- skip remediation task creation for this CVE (TC-8020); do not
   create any Tasks in Step 8. A Jira comment will be added explaining
   why task creation was skipped.
3. Proceed -- create remediation tasks anyway with a
   `concurrent-triage-overlap` label so the other engineer's Step 4.3
   cross-CVE overlap detection catches the overlap when they complete
   their triage of TC-8019
```

## Analysis

- **Option 1 (Wait)** is safest when the other triage is close to completion. After TC-8019's triage finishes and its remediation tasks are created, re-running Step 4.3 will detect whether those tasks already cover TC-8020's fix threshold (quinn-proto >= 0.11.14). This avoids creating duplicate bump tasks entirely.

- **Option 2 (Skip)** is appropriate if the engineer determines that TC-8019's remediation will definitively cover TC-8020 (e.g., both CVEs require bumping quinn-proto past the same or a higher threshold). Skipping adds a Jira comment for audit trail.

- **Option 3 (Proceed)** is appropriate when the engineer wants to ensure TC-8020 has its own remediation tasks regardless. The `concurrent-triage-overlap` label acts as a signal so that when TC-8019's engineer reaches their Step 4.3, they will detect the overlap and can deduplicate at that point.

## Timing

This concurrent triage check is executed at **Step 7**, which is positioned after Steps 3-6 (Affects Versions correction, duplicate/sibling/overlap checks, lifecycle checks, already-fixed checks) but **before** Step 8 (Case A/B/C remediation branching). The engineer must choose one of the three options before the skill proceeds to create remediation tasks.
