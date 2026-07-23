# Step 4.2 Triage Outcome: Pre-Existing Link Handling for TC-8006

## Summary

Step 4.2 (Cross-Stream Coordination) for TC-8006 detected sibling TC-8001 as a **different-stream companion** and correctly handled the pre-existing "Related" link by skipping link creation.

## Detailed Analysis

### Sibling Classification

- **TC-8006** stream suffix: `[rhtpa-2.1]` (stream 2.1.x)
- **TC-8001** stream suffix: `[rhtpa-2.2]` (stream 2.2.x)
- **Classification**: Different-stream companion -- NOT a duplicate

TC-8001 is a companion tracker for the same CVE (CVE-2026-31812) in a different product stream. PSIRT creates separate Vulnerability issues per stream by design. These issues should be linked with a "Related" relationship, not closed as duplicates.

### Step 4.2 Link Handling -- Idempotent Behavior

Per the skill procedure, Step 4.2 requires checking for existing links **before** creating new ones. The procedure specifies:

1. Read the current issue's `issuelinks` array from the `jira.get_issue` response (already fetched in Step 1).
2. Check if any existing link satisfies ALL of:
   - `type.name` is `"Related"`
   - `inwardIssue.key` or `outwardIssue.key` matches the sibling key

**What was found on TC-8006:**

The `issuelinks` array on TC-8006 contains one entry:
- Link ID: 1990401
- Type: Related
- Direction: outward (TC-8006 -> TC-8001)
- Linked issue: TC-8001

**Evaluation:**
- `type.name` = "Related" -- MATCHES
- `outwardIssue.key` = "TC-8001" -- MATCHES the sibling key

Both conditions are satisfied. A matching link already exists.

### Action Taken

> Related link to TC-8001 already exists -- skipping

Link creation was **skipped**. No `jira.create_link` call was made. This prevents creating a duplicate "Related" link between TC-8006 and TC-8001.

This is the correct idempotent behavior: the skill checks existing links before creating new ones, ensuring that re-running triage on an issue with pre-existing sibling links does not produce duplicate relationships in Jira.

### Sibling Landscape Still Presented

Even though the link already existed and link creation was skipped, the sibling landscape table was still presented to the engineer:

| Issue | Stream | Status | Affects Versions |
|-------|--------|--------|------------------|
| TC-8001 | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |
| TC-8006 (current) | 2.1.x | New | RHTPA 2.1.0 |

The landscape table is always shown regardless of link status because it provides valuable context about the overall CVE tracking across streams. Skipping the link creation does not skip the informational output.

### No Affects Versions Overlap

Each issue carries versions only from its own stream:
- TC-8006: RHTPA 2.1.0 (stream 2.1.x)
- TC-8001: RHTPA 2.2.0, RHTPA 2.2.1 (stream 2.2.x)

No overlap detected -- no engineer intervention required for version ownership.
