# Step 4 -- Duplicate, Sibling, and Overlap Check

## Step 4 -- Sibling Search

JQL query (simulated):
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

### Search Results

One sibling issue found:

| Field | Value |
|-------|-------|
| Issue Key | TC-8001 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Status | In Progress |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server |
| Affects Versions | RHTPA 2.2.0, RHTPA 2.2.1 |
| Stream Suffix | [rhtpa-2.2] |

### Sibling Classification

- **TC-8001** stream suffix: `[rhtpa-2.2]` (stream 2.2.x)
- **TC-8006** stream suffix: `[rhtpa-2.1]` (stream 2.1.x)
- Classification: **Different-stream companion** (not a duplicate)

TC-8001 is a cross-stream companion tracker, not a same-stream duplicate. PSIRT created one issue per stream intentionally. These are related issues tracking the same CVE in different version streams.

## Step 4.1 -- Same-Stream Duplicate Check

No same-stream siblings found. TC-8001 has stream suffix `[rhtpa-2.2]` which differs from TC-8006's `[rhtpa-2.1]`. No duplicate closure is warranted.

## Step 4.2 -- Cross-Stream Coordination

### Pre-existing Link Check

Before creating a Related link to sibling TC-8001, the issue's `issuelinks` array (fetched in Step 1) is inspected for an existing link.

**Existing issuelinks on TC-8006:**

| Link ID | Type | Direction | Linked Issue |
|---------|------|-----------|--------------|
| 1990401 | Related | outward | TC-8001 |

**Check criteria (all must match):**
1. `type.name` is "Related" -- YES (link type is Related)
2. `outwardIssue.key` or `inwardIssue.key` matches sibling key TC-8001 -- YES (outwardIssue.key = TC-8001)

**Result:** A matching Related link already exists (link ID 1990401, outward from TC-8006 to TC-8001).

> Related link to TC-8001 already exists -- skipping

Link creation is **skipped** because the idempotency check detected the pre-existing link. No duplicate link is created.

### Affects Versions Overlap Check

- TC-8006 Affects Versions: RHTPA 2.1.0 (stream 2.1.x)
- TC-8001 Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1 (stream 2.2.x)

No version overlap detected. Each issue carries only versions from its own stream, which is the correct state.

### Sibling Landscape

CVE-2026-31812 companion issues:

| Issue | Stream | Status | Affects Versions |
|-------|--------|--------|------------------|
| TC-8006 (current) | 2.1.x | New | RHTPA 2.1.0 |
| TC-8001 | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |

The sibling landscape table is presented despite the link already existing. The landscape provides the engineer with a complete view of how this CVE is tracked across all streams.

## Step 4.3 -- Cross-CVE Overlap Detection

Skipped. The Upstream Affected Component custom field, PS Component custom field, and Stream custom field are not configured in the project's Security Configuration. Step 4.3 requires all three fields to be present.

## Step 4.4 -- Preemptive Task Reconciliation

JQL query (simulated):
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```

No matching preemptive tasks found for CVE-2026-31812 in stream 2.1.x. Proceeding to Step 5.
