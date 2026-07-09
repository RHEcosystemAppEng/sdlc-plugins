# Step 7 -- Concurrent Triage Detection

## Prerequisite Check

The Upstream Affected Component custom field (customfield_10632) is configured in Security Configuration. The current issue TC-8020 has customfield_10632 = `quinn-proto`. Proceeding with concurrent triage detection.

## JQL Search

Search for in-progress triages on the same upstream component:

```
jira.search_jql(
  "project = TC AND issuetype = 10024 AND cf[10632] ~ 'quinn-proto' AND status IN ('In Progress', 'Code Review') AND key != TC-8020",
  fields: ["summary", "status", "labels", "assignee"]
)
```

## Search Results

The JQL search returned **1 result**:

| CVE Issue | Status | Assignee |
|-----------|--------|----------|
| TC-8019 | In Progress | engineer-b@example.com |

## Concurrent Triage Warning

**PROPOSED ACTION -- WARNING GATE:**

> **Concurrent triage detected** on the same upstream component (quinn-proto):
>
> | CVE Issue | Status | Assignee |
> |-----------|--------|----------|
> | TC-8019 | In Progress | engineer-b@example.com |
>
> Another engineer is actively triaging a related CVE. Creating remediation
> tasks now may produce duplicates.
>
> **Options:**
> 1. **Wait** -- pause until the other triage completes, then re-run Step 4.3 to detect any overlap
> 2. **Skip** -- skip remediation task creation for this CVE
> 3. **Proceed** -- create tasks anyway with a `concurrent-triage-overlap` label so the other engineer's Step 4.3 catches the overlap

## Handling

This warning gate runs **before** Case A/B/C branching in Step 8. No remediation tasks are created until the engineer selects one of the three options above.

- If the engineer chooses **Wait**: execution stops. The engineer should re-run triage after TC-8019's triage completes.
- If the engineer chooses **Skip**: Step 8 is skipped entirely. A Jira comment is posted on TC-8020 explaining why task creation was skipped due to concurrent triage on the same component.
- If the engineer chooses **Proceed**: the `concurrent-triage-overlap` label is added to TC-8020, and triage continues to Case A/B/C branching. The label ensures that TC-8019's Step 4.3 cross-CVE overlap detection can identify the overlap.
