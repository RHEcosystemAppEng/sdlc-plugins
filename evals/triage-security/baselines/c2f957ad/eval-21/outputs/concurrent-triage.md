# Step 7 – Concurrent Triage Detection: TC-8020

Protocol: `jira-triage-operations.md` — Step 7.

## Prerequisite check

- Upstream Affected Component custom field: **customfield_10632** — configured (per eval assumption). Step is NOT skipped.
- Field value on TC-8020 (from Step 1): **quinn-proto** — non-empty. Proceed.

## JQL search (simulated)

```
jira.search_jql(
  "project = TC AND issuetype = 10024 AND cf[10632] ~ 'quinn-proto' AND status IN ('In Progress', 'Code Review') AND key != TC-8020",
  fields: ["summary", "status", "labels", "assignee"]
)
```

Simulated result: **1 issue returned**.

## Result presented to the engineer

```
⚠️ Concurrent triage detected on the same upstream component (quinn-proto):

| CVE Issue | Status      | Assignee               |
|-----------|-------------|------------------------|
| TC-8019   | In Progress | engineer-b@example.com |

Another engineer is actively triaging a related CVE. Creating remediation
tasks now may produce duplicates.

Options:
1. Wait — pause until the other triage completes, then re-run Step 4.3
   to detect any overlap
2. Skip — skip remediation task creation for this CVE
3. Proceed — create tasks anyway with a `concurrent-triage-overlap` label
   so the other engineer's Step 4.3 catches the overlap
```

## Analysis

- TC-8019 is a different Vulnerability issue on the same upstream component (quinn-proto), actively In Progress and assigned to another engineer (engineer-b@example.com), not the current user. It therefore qualifies as a concurrent triage.
- Risk: both triages target quinn-proto in the RHTPA backend. If TC-8019's remediation bumps quinn-proto to >= 0.11.14 in the same stream(s), creating TC-8020 tasks now would duplicate that work (e.g. two `cargo update -p quinn-proto` tasks on `release/0.3.z`, plus duplicate downstream propagation tasks).
- Step 4.3 (cross-CVE overlap detection) could not catch this, because TC-8019's remediation tasks may not exist yet, and Step 4.3 would be skipped here anyway since the PS Component and Stream custom fields are not configured.

## Handling of each option

| Choice | Action |
|---|---|
| **Wait** | Stop execution; tell the engineer to re-run triage of TC-8020 after TC-8019 completes so Step 4.3 / 7.5.3 dedup can link to its remediation tasks. No Jira mutations. |
| **Skip** | Skip Step 8 (no remediation tasks). Post a Jira comment on TC-8020 (with Comment Footnote) explaining task creation was skipped due to concurrent triage TC-8019 on quinn-proto. |
| **Proceed** | Add the `concurrent-triage-overlap` label to TC-8020 (requires confirmation), then continue to Step 7.5 and Case A/B/C branching. |

## Decision status

The skill requires an explicit engineer choice before continuing to Step 7.5 / Case A/B/C ("Only continue to Case A/B/C after the user chooses"). No choice was given in this eval, so **triage is paused at Step 7 awaiting the engineer's decision**. No option was chosen automatically, and no label, comment, or task was created.

Recommended choice: **Wait** (or coordinate directly with engineer-b@example.com). TC-8019 is actively In Progress on the same crate, and waiting lets the existing dedup mechanisms (Step 4.3 / Step 7.5.3) reuse its remediation rather than duplicating it.
