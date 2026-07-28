# Step 4 -- Duplicate, Sibling, and Overlap Check

## 4.0 -- JQL Search for Sibling Issues

Search for sibling Vulnerability issues with the same CVE label:

```
jira.search_jql(
  "project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006"
)
```

**Results:** 1 sibling found.

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|------------------|---------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

## 4.1 -- Same-Stream Duplicate Check

Classify each sibling by stream scope:

- **TC-8006** (current issue): stream suffix `[rhtpa-2.1]` -> stream **2.1.x**
- **TC-8001** (sibling): stream suffix `[rhtpa-2.2]` -> stream **2.2.x**

**Classification:** TC-8001 is a **different-stream companion** (stream 2.2.x vs current issue's 2.1.x). This is NOT a same-stream duplicate.

No same-stream duplicates found. Proceeding to Step 4.2 (cross-stream coordination).

## 4.2 -- Cross-Stream Coordination

TC-8001 is a different-stream companion issue. PSIRT creates one Vulnerability issue per stream intentionally -- these are companion trackers, not duplicates.

### Idempotent link check

Before creating a "Related" link to TC-8001, check the current issue's existing `issuelinks` array (already fetched in Step 1):

**Existing links on TC-8006:**

| Link ID | Type | Direction | Linked Issue |
|---------|------|-----------|--------------|
| 1990401 | Related | outward (TC-8006 -> TC-8001) | TC-8001 |

**Check result:** A link exists where:
- `type.name` is "Related" -- **matches**
- `outwardIssue.key` is "TC-8001" -- **matches the sibling key**

**Decision: Related link to TC-8001 already exists -- skipping.**

The `jira.create_link` call is NOT executed because the pre-existing link already satisfies the cross-stream coordination requirement. This is an idempotent check -- if triage were run again, the same link would be detected and skipped again.

### Affects Versions overlap check

- **TC-8006** Affects Versions: RHTPA 2.1.0 (stream 2.1.x)
- **TC-8001** Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1 (stream 2.2.x)

No overlap detected -- each issue carries versions from its own stream only.

### Sibling Landscape Table

Despite the link already existing (and link creation being skipped), the sibling landscape is still presented to the engineer for context:

```
CVE-2026-31812 companion issues:

| Issue      | Stream | Status      | Affects Versions          |
|------------|--------|-------------|---------------------------|
| TC-8001    | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1  |
| TC-8006 <- | 2.1.x  | New         | RHTPA 2.1.0               |
```

The arrow `<-` marks the current issue being triaged.

The idempotent link check only affects whether `jira.create_link` is called -- it does not suppress the sibling summary table. The engineer needs to see the full companion issue landscape regardless of whether links were just created or already existed.

## 4.3 -- Cross-CVE Overlap Detection

The Upstream Affected Component custom field is not configured in Security Configuration (no `customfield_10632` entry). Skipping Step 4.3 entirely.

## 4.4 -- Preemptive Task Reconciliation

Search for preemptive remediation tasks matching CVE-2026-31812 for stream 2.1.x:

```
jira.search_jql(
  "project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC",
  fields: ["summary", "status", "labels", "issuelinks"]
)
```

**Results:** No matching preemptive tasks found for stream 2.1.x.

Proceeding to Step 5.
