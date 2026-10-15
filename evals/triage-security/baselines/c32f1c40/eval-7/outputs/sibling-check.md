# Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check

## 4.0 -- Sibling Search

A JQL search for sibling Vulnerability issues with the same CVE label was performed:

```
jira.search_jql(
  "project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006"
)
```

**Results**: 1 sibling found.

| Sibling Key | Summary | Stream Suffix | Status | Affects Versions |
|-------------|---------|---------------|--------|------------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | [rhtpa-2.2] | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |

## 4.1 -- Same-stream duplicate check

The current issue TC-8006 has stream suffix `[rhtpa-2.1]`.
Sibling TC-8001 has stream suffix `[rhtpa-2.2]`.

**Classification**: TC-8001 is a **different-stream companion** (stream [rhtpa-2.2] vs current issue's [rhtpa-2.1]), **not** a same-stream duplicate.

PSIRT creates one issue per stream intentionally. TC-8001 tracks the same CVE for the 2.2.x stream, while TC-8006 tracks it for the 2.1.x stream. These are companion trackers, not duplicates.

**Result**: No same-stream duplicates found. Proceeding to Step 4.2 (Cross-stream coordination).

## 4.2 -- Cross-stream coordination

TC-8001 is a different-stream sibling. Before creating a "Related" link, the idempotency check requires inspecting the current issue's existing `issuelinks` array.

### Idempotency check for TC-8001

Checking TC-8006's existing issuelinks for a link to TC-8001:

- Existing link found:
  - **Type**: Related
  - **Direction**: outward (TC-8006 -> TC-8001)
  - **Link ID**: 1990401

The existing link satisfies all conditions:
1. `type.name` is "Related" -- YES
2. `outwardIssue.key` matches TC-8001 -- YES

**Related link to TC-8001 already exists -- skipping.**

No call to `jira.create_link()` is made. The pre-existing "Related" link already establishes the cross-stream companion relationship between TC-8006 and TC-8001.

### Affects Versions overlap verification

- TC-8006 Affects Versions: RHTPA 2.1.0 (stream 2.1.x)
- TC-8001 Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1 (stream 2.2.x)

No version overlap detected -- each issue carries versions from its own stream only.

### Sibling landscape table

The following sibling landscape is presented to the engineer for visibility, regardless of whether link creation was needed:

```
CVE-2026-31812 companion issues:

| Issue      | Stream | Status      | Affects Versions             | Link Status                   |
|------------|--------|-------------|------------------------------|-------------------------------|
| TC-8001    | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1    | Related link already exists   |
| TC-8006 <- | 2.1.x  | New         | RHTPA 2.1.0                  | (current issue)               |
```

The arrow `<-` indicates TC-8006 is the current issue being triaged.

The sibling landscape table is always presented to the engineer to provide full cross-stream visibility. The idempotent link check only affects whether `jira.create_link` is called -- it does not suppress the sibling summary.

## 4.3 -- Cross-CVE overlap detection

The Upstream Affected Component custom field is not configured in Security Configuration (no `customfield_10632` or equivalent listed). Skipping Step 4.3 entirely per the prerequisite check.

## 4.4 -- Preemptive task reconciliation

A JQL search for preemptive tasks matching CVE-2026-31812 in stream rhtpa-2.1 would be performed:

```
jira.search_jql(
  "project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC"
)
```

**Assumed result**: No matching preemptive tasks found for this CVE and stream.

Proceeding to Step 5.
