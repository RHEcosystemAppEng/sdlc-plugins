# Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check

## Step 4 -- Sibling Search

JQL query executed (simulated):
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

### Sibling Issues Found

| Issue | Summary | Status | Stream Suffix | Affects Versions |
|-------|---------|--------|---------------|------------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | [rhtpa-2.2] | RHTPA 2.2.0, RHTPA 2.2.1 |

### Sibling Classification

- **TC-8006** stream suffix: `[rhtpa-2.1]` (stream 2.1.x)
- **TC-8001** stream suffix: `[rhtpa-2.2]` (stream 2.2.x)

**Classification: Different-stream companion** -- TC-8001 is scoped to stream 2.2.x while TC-8006 is scoped to stream 2.1.x. These are companion trackers for the same CVE across different streams, NOT same-stream duplicates. PSIRT creates one issue per stream intentionally.

## Step 4.1 -- Same-Stream Duplicate Check

No same-stream siblings found. TC-8001 belongs to a different stream (2.2.x vs 2.1.x). No duplicate closure recommended.

## Step 4.2 -- Cross-Stream Coordination

### Pre-existing Link Check

Before attempting to create a "Related" link to sibling TC-8001, the current issue's existing `issuelinks` array (fetched in Step 1) was inspected.

**Existing issuelinks on TC-8006:**

| Link ID | Type | Direction | Linked Issue |
|---------|------|-----------|-------------|
| 1990401 | Related | outward (TC-8006 -> TC-8001) | TC-8001 |

**Check result:** A link matching ALL of the following criteria was found:
- `type.name` is `"Related"` -- YES
- `outwardIssue.key` matches the sibling key `TC-8001` -- YES

**Related link to TC-8001 already exists -- skipping link creation.** The pre-existing Related link (ID: 1990401) already connects TC-8006 to TC-8001. Creating another link would be a duplicate, so `jira.create_link` is NOT called.

### Affects Versions Overlap Check

- TC-8006 Affects Versions: RHTPA 2.1.0 (stream 2.1.x)
- TC-8001 Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1 (stream 2.2.x)

No Affects Versions overlap detected -- each issue correctly carries only versions from its own stream.

### Sibling Landscape

Despite the link already existing, the sibling landscape is presented to the engineer for context:

```
CVE-2026-31812 companion issues:

| Issue      | Stream | Status      | Affects Versions              |
|------------|--------|-------------|-------------------------------|
| TC-8001    | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1     |
| TC-8006 <  | 2.1.x  | New         | RHTPA 2.1.0                   |
```

The arrow (`<`) indicates the current issue being triaged. TC-8001 is already in progress on stream 2.2.x, providing context that remediation for this CVE is actively underway for the 2.2.x stream.
