# Triage Outcome -- Step 4.2 Pre-Existing Link Handling: TC-8006

## Summary

Step 4.2 (Cross-Stream Coordination) correctly identified that a Related link between TC-8006 and its sibling TC-8001 already exists and skipped link creation. This demonstrates the idempotent link-creation behavior specified in the triage-security skill.

## Step 4.2 Detailed Walkthrough

### 1. Sibling Classification

TC-8001 was identified as a **different-stream companion** (not a duplicate):
- TC-8006 stream: `[rhtpa-2.1]` (2.1.x)
- TC-8001 stream: `[rhtpa-2.2]` (2.2.x)

Different stream suffixes mean these are companion trackers. PSIRT creates one Vulnerability issue per stream intentionally.

### 2. Pre-Existing Link Detection

Per the Step 4.2 procedure in `jira-triage-operations.md`:

> "Check for existing link before creating one. Read the current issue's issuelinks array from the jira.get_issue response (already fetched in Step 1). Check if any existing link satisfies all of:
> - type.name is "Related"
> - inwardIssue.key or outwardIssue.key matches the sibling key"

TC-8006's `issuelinks` array contains:

```
- Link ID: 1990401
  Type: Related
  Direction: outward (TC-8006 -> TC-8001)
```

This link satisfies both conditions:
- `type.name` is "Related" -- matched
- `outwardIssue.key` is TC-8001 -- matched against the sibling key

### 3. Link Creation Skipped

Because the existing link satisfies all conditions, the skill follows the specified behavior:

> "If a matching link exists, skip link creation and log:
> 'Related link to [sibling-key] already exists -- skipping'"

**Log message**: Related link to TC-8001 already exists -- skipping

No `jira.create_link` call is made. This prevents duplicate links and ensures idempotent behavior when re-triaging or when PSIRT has pre-linked companion issues.

### 4. Sibling Landscape Still Presented

Despite skipping link creation, the sibling landscape table is still presented to the engineer for awareness:

```
CVE-2026-31812 companion issues:

| Issue      | Stream | Status      | Affects Versions              |
|------------|--------|-------------|-------------------------------|
| TC-8001    | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1     |
| TC-8006 <- | 2.1.x  | New         | RHTPA 2.1.0                   |
```

The landscape table is informational and always presented regardless of whether a link was created or already existed. It gives the engineer visibility into the full CVE tracking picture across streams.

### 5. No Affects Versions Overlap

The two issues carry versions from different streams with no overlap:
- TC-8006: RHTPA 2.1.0 (stream 2.1.x)
- TC-8001: RHTPA 2.2.0, RHTPA 2.2.1 (stream 2.2.x)

No version overlap flag is raised.

## Why This Matters

The idempotent link check in Step 4.2 handles several real-world scenarios:

1. **PSIRT pre-linking**: PSIRT may pre-link companion issues when creating them, as in this case.
2. **Re-triage**: If an issue is triaged a second time, duplicate links are prevented.
3. **Concurrent triage**: If two engineers triage companion issues simultaneously, the second triage does not create a redundant link.

The skill's behavior matches the procedure specification exactly: check existing links first, skip if already present, log the skip, and continue with the remaining Step 4.2 procedures (overlap check, landscape presentation).
