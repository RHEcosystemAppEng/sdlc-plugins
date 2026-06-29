# Triage Outcome -- Step 4.2 Pre-existing Link Handling

## Summary

TC-8006 (CVE-2026-31812, stream [rhtpa-2.1]) has a pre-existing Related link to TC-8001 (stream [rhtpa-2.2]). Step 4.2 correctly detected this link and skipped link creation, demonstrating idempotent behavior.

## Step 4.2 Detailed Walkthrough

### 1. Sibling Identified

The JQL search for sibling issues with label `CVE-2026-31812` returned one result: TC-8001 with stream suffix `[rhtpa-2.2]`. Since `[rhtpa-2.2]` differs from TC-8006's `[rhtpa-2.1]`, TC-8001 is classified as a **different-stream companion**, not a same-stream duplicate.

### 2. Existing Link Inspection (Idempotency Check)

Per Step 4.2 of `jira-triage-operations.md`, before creating a Related link the skill must check the current issue's `issuelinks` array (already fetched in Step 1 via `jira.get_issue`).

The `issuelinks` array on TC-8006 contains:

```
{
  "id": "1990401",
  "type": { "name": "Related" },
  "outwardIssue": { "key": "TC-8001" }
}
```

The check evaluates two criteria:
1. **`type.name` is "Related"** -- matches (the link type is "Related")
2. **`outwardIssue.key` matches the sibling key** -- matches (outwardIssue.key is "TC-8001")

Both criteria are satisfied. The pre-existing link is a valid Related link to the sibling.

### 3. Link Creation Skipped

Because a matching Related link already exists, link creation is skipped. The logged message is:

> "Related link to TC-8001 already exists -- skipping"

This prevents duplicate links from being created if the skill is re-run or if the link was manually created before triage.

### 4. Sibling Landscape Still Presented

Even though link creation was skipped, the sibling landscape table is still presented to the engineer. The landscape provides essential cross-stream context regardless of whether a new link was just created or an existing one was found:

| Issue | Stream | Status | Affects Versions |
|-------|--------|--------|------------------|
| TC-8006 (current) | 2.1.x | New | RHTPA 2.1.0 |
| TC-8001 | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |

### 5. No Version Overlap

The Affects Versions between the two issues do not overlap:
- TC-8006: RHTPA 2.1.0 (belongs to stream 2.1.x)
- TC-8001: RHTPA 2.2.0, RHTPA 2.2.1 (belongs to stream 2.2.x)

Each issue correctly carries only versions from its own stream.

## Key Behaviors Demonstrated

1. **Idempotent link handling**: The skill checks `issuelinks` before calling `jira.create_link`, avoiding duplicate Related links.
2. **Pre-existing link detection**: The outward Related link (TC-8006 -> TC-8001, link ID 1990401) was detected by matching both `type.name == "Related"` and `outwardIssue.key == "TC-8001"`.
3. **Skip with log**: When the link already exists, the skill logs "Related link to TC-8001 already exists -- skipping" and does not attempt to create a new link.
4. **Landscape still shown**: The sibling landscape table is presented regardless of whether link creation was performed or skipped. The table provides cross-stream visibility.
5. **Companion, not duplicate**: TC-8001 (stream [rhtpa-2.2]) is correctly identified as a different-stream companion to TC-8006 (stream [rhtpa-2.1]). Different-stream siblings are never treated as duplicates -- PSIRT creates separate issues per stream intentionally.
