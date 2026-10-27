# Step 7 -- Concurrent Triage Detection

## Prerequisite Check

- Upstream Affected Component custom field: **configured** (customfield_10632)
- Current issue (TC-8020) Upstream Affected Component value: **quinn-proto**

Since the Upstream Affected Component custom field is configured and populated, Step 7 proceeds.

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

## Analysis

A concurrent triage has been detected on the same upstream component (quinn-proto). TC-8019 is actively being triaged by engineer-b@example.com and is currently In Progress. Creating remediation tasks now for TC-8020 may produce duplicate remediation tasks if TC-8019's triage also reaches Step 8 and creates tasks targeting the same quinn-proto dependency bump.

## Warning Presented

```
WARNING: Concurrent triage detected on the same upstream component (quinn-proto):

| CVE Issue | Status      | Assignee                 |
|-----------|-------------|--------------------------|
| TC-8019   | In Progress | engineer-b@example.com   |

Another engineer is actively triaging a related CVE that affects the same
upstream component. Creating remediation tasks now may produce duplicates.

Options:
1. Wait -- pause until the other triage (TC-8019) completes, then re-run
   Step 4.3 to detect any overlap from TC-8019's remediation tasks
2. Skip -- skip remediation task creation for this CVE entirely and add a
   Jira comment explaining why task creation was skipped
3. Proceed -- create tasks anyway with a `concurrent-triage-overlap` label
   so that engineer-b's Step 4.3 (cross-CVE overlap detection) catches the
   overlap when TC-8019's triage completes
```

## Timing in Workflow

This concurrent triage check occurs **after** Steps 1-6 (data extraction, version impact analysis, Affects Versions correction, duplicate/sibling/overlap check, lifecycle check, and already-fixed check) and **before** Step 7.5 (Release Jira Orchestration) and Step 8 (Case A/B/C remediation branching).

The engineer must choose one of the three options before the skill continues to Case A/B/C branching:

- **Option 1 (Wait)**: Execution stops. The engineer re-runs triage after TC-8019 completes. At that point, Step 4.3 cross-CVE overlap detection would identify whether TC-8019's remediation tasks already cover quinn-proto >= 0.11.14, potentially eliminating the need for new tasks.

- **Option 2 (Skip)**: Step 8 is skipped entirely. No remediation tasks are created. A Jira comment is posted to TC-8020 explaining that task creation was skipped due to concurrent triage on the same upstream component (quinn-proto) by TC-8019.

- **Option 3 (Proceed)**: The `concurrent-triage-overlap` label is added to TC-8020, and triage continues to Step 7.5 and Step 8 (Case A/B/C). The label ensures that when TC-8019's triage reaches Step 4.3 (cross-CVE overlap detection), it will detect the overlap and either reuse TC-8020's remediation tasks or flag the duplication.
