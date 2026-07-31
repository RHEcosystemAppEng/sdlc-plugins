# Step 7 -- Concurrent Triage Detection for TC-8020

## Prerequisite Check

The Upstream Affected Component custom field (`customfield_10632`) is configured in Security Configuration. The current issue TC-8020 has `customfield_10632` set to `quinn-proto`. Proceeding with concurrent triage detection.

## JQL Search

Query executed (simulated):

```
project = TC AND issuetype = 10024 AND cf[10632] ~ 'quinn-proto' AND status IN ('In Progress', 'Code Review') AND key != TC-8020
```

Fields requested: summary, status, labels, assignee

## Results

The JQL search returned **1 result**:

| CVE Issue | Status | Assignee |
|-----------|--------|----------|
| TC-8019   | In Progress | engineer-b@example.com |

## Concurrent Triage Warning

**Concurrent triage detected on the same upstream component (quinn-proto):**

Another engineer (engineer-b@example.com) is actively triaging TC-8019, which affects the same upstream component `quinn-proto`. TC-8019 is currently In Progress, meaning that engineer is between Step 0.7 (assignment) and Step 8 (remediation). Creating remediation tasks now may produce duplicates if both triages reach Step 8 simultaneously.

## Options Presented to Engineer

1. **Wait** -- pause until the other triage (TC-8019) completes, then re-run Step 4.3 to detect any overlap from TC-8019's remediation tasks. This is the safest option to avoid duplicate remediation tasks.

2. **Skip** -- skip remediation task creation for this CVE (TC-8020). Do not create remediation tasks in Step 8. Add a Jira comment explaining why task creation was skipped due to concurrent triage on the same component.

3. **Proceed** -- create tasks anyway with a `concurrent-triage-overlap` label added to the current issue (TC-8020), so that the other engineer's Step 4.3 (cross-CVE overlap detection) catches the overlap when they reach it. This allows both triages to continue independently while flagging the potential overlap for reconciliation.

## Execution Position

This step (Step 7) executes **after** Steps 3-6 (Affects Versions Correction, Duplicate/Sibling/Overlap Check, Version Lifecycle Check, Already Fixed Check) and **before** Step 8 Case A/B/C branching (remediation task creation or close). The concurrent triage check acts as a gate: only after the user selects an option does the workflow proceed to (or skip) Case A/B/C.

Per the SKILL.md flowchart:
```
A["Version impact table (after Steps 4-6)"] --> Z{"Step 7: Concurrent triage on same component?"}
Z -->|No or user proceeds| B{"Any supported versions affected?"}
Z -->|User waits/skips| STOP["Stop or skip task creation"]
```

The user must choose one of the three options before the skill can proceed to Case A/B/C branching in Step 8.
