# Step 7 – Concurrent Triage Detection: TC-8020

Protocol: `jira-triage-operations.md` — Step 7.

## Prerequisite check

- Upstream Affected Component custom field: **customfield_10632** — configured in Security
  Configuration (per eval assumption). Step 7 is **not** skipped.
- Value on TC-8020: **quinn-proto** (non-empty). Proceed with the search.

## JQL search (simulated — not executed against Jira)

```
jira.search_jql(
  "project = TC AND issuetype = 10024 AND cf[10632] ~ 'quinn-proto' AND status IN ('In Progress', 'Code Review') AND key != TC-8020",
  fields: ["summary", "status", "labels", "assignee"]
)
```

## Result (simulated)

One result returned:

| CVE Issue | Status | Assignee |
|---|---|---|
| TC-8019 | In Progress | engineer-b@example.com |

## Warning presented to the engineer

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

- TC-8019 is a different Vulnerability issue on the same upstream component (quinn-proto)
  and is actively In Progress under another engineer (engineer-b@example.com). It is
  not assigned to the current user, so it counts as a genuine concurrent triage.
- TC-8020 needs remediation on 2.2.x (2.2.0–2.2.2 ship quinn-proto < 0.11.14), and 2.1.x is
  also affected (cross-stream, Case A). Both paths would create quinn-proto bump tasks for
  the backend Cargo dependency, which is very likely what TC-8019 will create too. A
  single bump to quinn-proto >= 0.11.14 per stream would probably fix both CVEs, so
  creating tasks now risks duplicates.
- Step 7.5.3 (cross-CVE dedup against tasks already linked to the release Task) only finds
  tasks that already exist. TC-8019 has not created its tasks yet, so dedup would not
  stop the duplicates. That is the gap Step 7 exists to cover.

## Handling of each option

| Choice | Action |
|---|---|
| Wait | Stop execution now; tell the engineer to re-run triage of TC-8020 once TC-8019 finishes, at which point Step 4.3 / 7.5.3 will detect its remediation tasks and link instead of duplicating. |
| Skip | Skip Step 8 entirely (no remediation tasks); post a Jira comment on TC-8020 (with Comment Footnote) explaining task creation was skipped because of concurrent triage TC-8019 on quinn-proto. |
| Proceed | Add label `concurrent-triage-overlap` to TC-8020 (with confirmation), then continue to Step 7.5 and Case A/B/C branching. |

## Recommendation

**Option 1 – Wait.** Same component, other triage actively In Progress, high chance the
fix is the same. Per the protocol, execution does **not** continue to Step 7.5 / Case A/B/C
until the engineer chooses. In this eval no engineer reply is available, so triage stops
at this gate.
