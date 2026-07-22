# Triage Outcome -- Step 4.2 Pre-Existing Link Handling

## Summary

TC-8006 (CVE-2026-31812, stream [rhtpa-2.1]) has a pre-existing "Related" link to sibling issue TC-8001 (stream [rhtpa-2.2]). Step 4.2 handled this through its **idempotent link creation** protocol.

## How Step 4.2 Handled the Pre-Existing Link

### The Idempotent Check

Step 4.2 specifies that before creating a "Related" link to a cross-stream sibling, the skill must first read the current issue's `issuelinks` array (already fetched in Step 1's `jira.get_issue` call) and check whether a link already exists that satisfies **all** of:

1. `type.name` is `"Related"`
2. `inwardIssue.key` or `outwardIssue.key` matches the sibling key

### Application to TC-8006

TC-8006's `issuelinks` array contains an existing link:
- **type.name**: `Related`
- **outwardIssue.key**: `TC-8001`
- **Link ID**: 1990401
- **Direction**: outward (TC-8006 -> TC-8001)

Both criteria are satisfied:
- Criterion 1: type.name `"Related"` matches -- **satisfied**
- Criterion 2: outwardIssue.key `"TC-8001"` matches the sibling key -- **satisfied**

### Outcome

**Link creation was skipped.** The skill logged:

> "Related link to TC-8001 already exists -- skipping"

No Jira mutation occurred for this link. This is the correct idempotent behavior -- re-running triage on an issue that already has sibling links does not create duplicate links or produce errors. The existing link (ID 1990401) remains unchanged.

### Why This Matters

The idempotent check prevents:
- **Duplicate links** -- Jira may reject or create redundant links if the same Related link is created twice
- **Unnecessary API calls** -- skipping the `jira.create_link` call avoids a wasted round-trip
- **Audit confusion** -- a single clean Related link between companions is clearer than multiples

### Remaining Step 4.2 Actions

After the link check, Step 4.2 continued with:

1. **Affects Versions overlap check** -- no overlap found. TC-8006 carries only RHTPA 2.1.0 (stream 2.1.x) and TC-8001 carries RHTPA 2.2.0 and RHTPA 2.2.1 (stream 2.2.x). Each issue owns only its own stream's versions.

2. **Sibling landscape presentation** -- the companion issue table was presented showing both issues, their streams, statuses, and Affects Versions, with TC-8006 marked as the current issue.

## Context: Full Step 4 Flow

| Sub-step | Action | Result |
|----------|--------|--------|
| 4.1 | Same-stream duplicate check | No duplicates (TC-8001 is different-stream) |
| 4.2 | Cross-stream coordination | Pre-existing Related link to TC-8001 found; link creation skipped (idempotent); no Affects Versions overlap |
| 4.3 | Cross-CVE overlap detection | Skipped (Upstream Affected Component field not configured) |
| 4.4 | Preemptive task reconciliation | No preemptive tasks found for CVE-2026-31812 in stream 2.1.x |
