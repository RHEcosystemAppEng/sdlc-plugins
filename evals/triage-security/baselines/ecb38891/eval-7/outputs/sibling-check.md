# Step 4 -- Duplicate, Sibling, and Overlap Check

## Step 4 -- Sibling Search

Search for sibling Vulnerability issues with the same CVE label:

```
jira.search_jql(
  "project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006"
)
```

**Results:** 1 sibling issue found.

| Sibling Key | Summary | Status | Stream Suffix | Affects Versions |
|-------------|---------|--------|---------------|------------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | [rhtpa-2.2] | RHTPA 2.2.0, RHTPA 2.2.1 |

## Sibling Classification

Current issue TC-8006 has stream suffix **[rhtpa-2.1]** (stream 2.1.x).
Sibling TC-8001 has stream suffix **[rhtpa-2.2]** (stream 2.2.x).

**Classification: Different-stream companion** (not a same-stream duplicate).

The stream suffixes differ ([rhtpa-2.1] vs [rhtpa-2.2]), so TC-8001 is a companion tracker for a different version stream. PSIRT creates one Vulnerability issue per stream intentionally -- these are not duplicates.

### Step 4.1 -- Same-Stream Duplicate Check

No same-stream siblings found. TC-8001 is in a different stream (2.2.x vs 2.1.x). No duplicate detection triggered.

### Step 4.2 -- Cross-Stream Coordination

TC-8001 is a different-stream companion. Per Step 4.2, before creating a "Related" link, check the current issue's existing `issuelinks` array.

**Existing issuelinks on TC-8006 (from Step 1 data extraction):**

| Link Type | Direction | Linked Issue |
|-----------|-----------|--------------|
| Related | outward | TC-8001 |

**Idempotency check:** Inspecting TC-8006's existing issuelinks for a link where:
- `type.name` is `"Related"`
- `outwardIssue.key` matches `TC-8001`

**Result:** A matching link is found (Link ID: 1990401, type: Related, direction: outward, target: TC-8001).

> Related link to TC-8001 already exists -- skipping

The `jira.create_link` call is **NOT** executed. The pre-existing Related link satisfies the idempotency check, so link creation is skipped to avoid a duplicate link.

### Affects Versions Overlap Check

Verifying no Affects Versions overlap between TC-8006 and TC-8001:

- TC-8006 Affects Versions: RHTPA 2.1.0 (stream 2.1.x)
- TC-8001 Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1 (stream 2.2.x)

No overlap detected -- each issue carries versions from its own stream only.

### Sibling Landscape Table

Despite the link already existing (and link creation being skipped), the sibling landscape is still presented to the engineer for visibility:

```
CVE-2026-31812 companion issues:

| Issue       | Stream | Status      | Affects Versions           |
|-------------|--------|-------------|----------------------------|
| TC-8001     | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1  |
| TC-8006 <-- | 2.1.x  | New         | RHTPA 2.1.0               |
```

The arrow (`<--`) marks the current issue being triaged.

**Note:** The idempotent link check only affects link creation -- it does not suppress the sibling summary table. The engineer always sees the full companion landscape regardless of whether links were created or skipped.

## Step 4.3 -- Cross-CVE Overlap Detection

The Upstream Affected Component custom field is not configured in the Security Configuration (no `customfield_10632` or equivalent field specified). Step 4.3 is skipped entirely.

## Step 4.4 -- Preemptive Task Reconciliation

Search for preemptive tasks matching the current CVE and stream:

```
jira.search_jql(
  "project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC"
)
```

Filter results for tasks whose summary contains the stream name "rhtpa-2.1".

**Assumed result:** No matching preemptive tasks found.

Proceeding to Step 5 (Version Lifecycle Check).
