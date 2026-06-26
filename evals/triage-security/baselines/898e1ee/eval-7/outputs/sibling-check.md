# Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check

## Step 4 -- JQL Sibling Search

Search query (simulated):
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

### Search Results

One sibling issue found:

| Field | Value |
|-------|-------|
| Key | TC-8001 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Status | In Progress |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server |
| Affects Versions | RHTPA 2.2.0, RHTPA 2.2.1 |
| Stream suffix | [rhtpa-2.2] |

### Classification

- **TC-8006** stream suffix: `[rhtpa-2.1]` (stream 2.1.x)
- **TC-8001** stream suffix: `[rhtpa-2.2]` (stream 2.2.x)

TC-8001 is a **different-stream companion** (stream [rhtpa-2.2] vs current [rhtpa-2.1]). This is NOT a duplicate. PSIRT creates one issue per stream intentionally.

## Step 4.1 -- Same-Stream Duplicate Check

No same-stream siblings found. TC-8001 has a different stream suffix (`[rhtpa-2.2]` vs `[rhtpa-2.1]`), so it is not a same-stream duplicate.

Result: No duplicates detected. Proceed to Step 4.2.

## Step 4.2 -- Cross-Stream Coordination

### Existing Link Check (Idempotent)

Before creating a "Related" link to TC-8001, checking the current issue's `issuelinks` array (fetched in Step 1).

Existing issue links on TC-8006:
- Link ID 1990401: Type = "Related", outwardIssue.key = "TC-8001"

Check criteria:
- `type.name` is "Related"? **YES**
- `outwardIssue.key` matches sibling key "TC-8001"? **YES**

**Related link to TC-8001 already exists -- skipping link creation.**

> Related link to TC-8001 already exists -- skipping

### Affects Versions Overlap Check

- TC-8006 (stream 2.1.x): Affects Versions = [RHTPA 2.1.0]
- TC-8001 (stream 2.2.x): Affects Versions = [RHTPA 2.2.0, RHTPA 2.2.1]

No version overlap detected. Each issue carries only versions from its own stream. This is correct.

### Sibling Landscape

Despite the link already existing (no new link created), the sibling landscape is still presented for the engineer's awareness:

```
CVE-2026-31812 companion issues:

| Issue       | Stream | Status      | Affects Versions              |
|-------------|--------|-------------|-------------------------------|
| TC-8006 <-  | 2.1.x  | New         | RHTPA 2.1.0                   |
| TC-8001     | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1     |
```

The arrow (`<-`) marks the current issue being triaged.

### Summary

- Sibling TC-8001 is a cross-stream companion for stream 2.2.x (already In Progress)
- A "Related" link between TC-8006 and TC-8001 already exists (link ID 1990401) -- no new link was created
- No Affects Versions overlap between the two issues
- The idempotent check prevented duplicate link creation while still presenting the full sibling landscape to the engineer
