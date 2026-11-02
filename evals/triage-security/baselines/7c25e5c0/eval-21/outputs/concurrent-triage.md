# Step 7 — Concurrent Triage Detection

## Prerequisite Check

The Upstream Affected Component custom field is configured in Security Configuration. Proceeding with concurrent triage detection.

## Upstream Affected Component Extraction

Extracted from TC-8020's `customfield_10632`: **quinn-proto**

## JQL Search for In-Progress Triages

Query:
```
project = TC AND issuetype = 10024 AND cf[10632] ~ 'quinn-proto' AND status IN ('In Progress', 'Code Review') AND key != TC-8020
```

### Search Results

| CVE Issue | Status | Assignee |
|-----------|--------|----------|
| TC-8019 | In Progress | engineer-b@example.com |

## Concurrent Triage Warning

⚠️ **Concurrent triage detected on the same upstream component (quinn-proto):**

| CVE Issue | Status | Assignee |
|-----------|--------|----------|
| TC-8019 | In Progress | engineer-b@example.com |

Another engineer is actively triaging a related CVE that affects the same upstream component (`quinn-proto`). Creating remediation tasks now may produce duplicates if both triages independently create bump/backport tasks for the same library.

**Options:**

1. **Wait** — pause until TC-8019's triage completes, then re-run Step 4.3 to detect any overlap. This is the safest option to avoid duplicate remediation tasks.
2. **Skip** — skip remediation task creation for this CVE entirely. A Jira comment will be added explaining why task creation was skipped.
3. **Proceed** — create tasks anyway with a `concurrent-triage-overlap` label so that TC-8019's Step 4.3 cross-CVE overlap detection can catch the overlap and reconcile.

Awaiting engineer choice before proceeding to Case A/B/C branching in Step 8.
