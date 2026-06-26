# Triage Outcome -- Step 4.2 Pre-Existing Link Handling

## Context

TC-8006 (CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.1]) has a pre-existing "Related" link to TC-8001 (CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]).

## How Step 4.2 Handled the Pre-Existing Link

### The Idempotent Check

Step 4.2 requires checking for existing links before creating new ones. The procedure is:

1. Read the current issue's `issuelinks` array from the `jira.get_issue` response (already fetched in Step 1).
2. For each different-stream sibling, check if any existing link satisfies ALL of:
   - `type.name` is `"Related"`
   - `inwardIssue.key` or `outwardIssue.key` matches the sibling key

### Application to TC-8006

The issue's existing links (from Step 1 data extraction) include:

- Link ID: 1990401
- Type: Related
- Direction: outward (TC-8006 -> TC-8001)

When processing sibling TC-8001:
- Check: Does any existing link have `type.name == "Related"`? **Yes** (link ID 1990401)
- Check: Does `outwardIssue.key` match "TC-8001"? **Yes**
- Both conditions satisfied.

**Result: Related link to TC-8001 already exists -- skipping link creation.**

No `jira.create_link` call was made. This prevents duplicate links from being created if the skill is run multiple times or if links were manually created before triage.

### What Was NOT Skipped

The idempotent check only affects **link creation**. The following Step 4.2 activities were still performed:

1. **Affects Versions overlap check** -- verified that TC-8006 and TC-8001 do not share any Affects Versions entries (they do not: TC-8006 has RHTPA 2.1.0, TC-8001 has RHTPA 2.2.0 and RHTPA 2.2.1)
2. **Sibling landscape table** -- the full companion issues table was presented to the engineer, showing both TC-8006 (2.1.x, New) and TC-8001 (2.2.x, In Progress) with their respective Affects Versions

### Why This Matters

The idempotent link check ensures that:
- Re-running triage on an already-partially-triaged issue does not create duplicate "Related" links
- Manually pre-linked issues are handled gracefully
- The engineer still receives the full sibling context regardless of whether a new link was created

### Sibling Classification

TC-8001 is classified as a **different-stream companion** (not a duplicate) because:
- TC-8006 has stream suffix `[rhtpa-2.1]` (stream 2.1.x)
- TC-8001 has stream suffix `[rhtpa-2.2]` (stream 2.2.x)
- Different streams mean different companion trackers, not duplicates
- TC-8001 is already "In Progress", indicating active remediation on the 2.2.x stream
