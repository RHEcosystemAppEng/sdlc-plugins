# Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check: TC-8006

## Step 4 -- JQL Sibling Search

Search query:
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

**Results: 1 sibling found.**

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|------------------|---------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

## Step 4 -- Sibling Classification

Current issue TC-8006 has stream suffix `[rhtpa-2.1]` (stream 2.1.x).
Sibling TC-8001 has stream suffix `[rhtpa-2.2]` (stream 2.2.x).

**Classification: Different-stream companion (NOT a duplicate).**

Rationale: The two issues track the same CVE (CVE-2026-31812) but for different product version streams. PSIRT creates one Vulnerability issue per stream intentionally. TC-8001 covers stream 2.2.x while TC-8006 covers stream 2.1.x -- these are companion trackers, not duplicates.

## Step 4.1 -- Same-Stream Duplicate Check

No same-stream siblings found. TC-8001 is in a different stream (2.2.x vs 2.1.x). No duplicate closure warranted.

## Step 4.2 -- Cross-Stream Coordination

### Link Check for TC-8001

Before creating a "Related" link to sibling TC-8001, checking the current issue's existing `issuelinks` array (fetched in Step 1 via `jira.get_issue`).

**Existing links on TC-8006:**

| Link ID | Type | Direction | Linked Issue |
|---------|------|-----------|--------------|
| 1990401 | Related | outward | TC-8001 |

**Link evaluation:**
- Type name: `Related` -- matches required type
- Outward issue key: `TC-8001` -- matches the sibling key

**Result: Pre-existing "Related" link to TC-8001 found.**

> Related link to TC-8001 already exists -- skipping

Link creation is skipped to avoid creating a duplicate link. The existing link (ID: 1990401) already satisfies the cross-stream coordination requirement.

### Affects Versions Overlap Check

- TC-8006 Affects Versions: RHTPA 2.1.0 (stream 2.1.x)
- TC-8001 Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1 (stream 2.2.x)

No version overlap detected. Each issue carries only versions from its own stream.

### Sibling Landscape

CVE-2026-31812 companion issues:

| Issue | Stream | Status | Affects Versions |
|-------|--------|--------|------------------|
| TC-8001 | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |
| TC-8006 (current) | 2.1.x | New | RHTPA 2.1.0 |

The sibling landscape is presented despite the link already existing, as it provides useful context for the engineer about the overall CVE tracking status across streams.
