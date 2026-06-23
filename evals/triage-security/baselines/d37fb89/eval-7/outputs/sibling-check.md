# Step 4 -- Duplicate, Sibling, and Overlap Check for TC-8006

## Step 4 -- JQL Sibling Search

### Query

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

### Results

One sibling found:

| Field | Value |
|-------|-------|
| Issue Key | TC-8001 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Status | In Progress |
| Stream suffix | [rhtpa-2.2] |
| Affects Versions | RHTPA 2.2.0, RHTPA 2.2.1 |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server |

## Step 4.1 -- Same-Stream Duplicate Check

TC-8001 has stream suffix `[rhtpa-2.2]`, which maps to stream **2.2.x**.
TC-8006 has stream suffix `[rhtpa-2.1]`, which maps to stream **2.1.x**.

These are **different streams** -- TC-8001 is NOT a same-stream duplicate. It is a cross-stream companion tracker. PSIRT intentionally creates one Vulnerability issue per stream.

Result: **No same-stream duplicates found.** Proceed to Step 4.2.

## Step 4.2 -- Cross-Stream Coordination

TC-8001 is a **different-stream sibling** (companion tracker for the 2.2.x stream).

### Link Check (Idempotent)

Before creating a "Related" link, the skill checks TC-8006's existing `issuelinks` array from the Step 1 `jira.get_issue` response.

**Existing links on TC-8006:**
- Link ID: 1990401
  - Type: Related
  - Direction: outward (TC-8006 -> TC-8001)
  - Target: TC-8001

**Check result:** A link matching ALL of the following criteria already exists:
1. `type.name` is "Related" -- YES (type is "Related")
2. `outwardIssue.key` matches the sibling key TC-8001 -- YES

**Decision: Related link to TC-8001 already exists -- skipping link creation.**

No `jira.create_link` call is made. This is the idempotent behavior specified in Step 4.2: when a matching Related link already exists (in either direction -- inward or outward), the skill skips link creation rather than creating a duplicate link.

### Affects Versions Overlap Check

| Issue | Stream | Affects Versions |
|-------|--------|------------------|
| TC-8006 | 2.1.x | RHTPA 2.1.0 |
| TC-8001 | 2.2.x | RHTPA 2.2.0, RHTPA 2.2.1 |

No version overlap detected. Each issue carries versions only from its own stream:
- TC-8006 owns 2.1.x versions (RHTPA 2.1.0)
- TC-8001 owns 2.2.x versions (RHTPA 2.2.0, RHTPA 2.2.1)

This is correct -- no overlap flag needed.

### Sibling Landscape

```
CVE-2026-31812 companion issues:

| Issue       | Stream | Status      | Affects Versions              |
|-------------|--------|-------------|-------------------------------|
| TC-8001     | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1     |
| TC-8006 <-  | 2.1.x  | New         | RHTPA 2.1.0                   |
```

The arrow `<-` marks the current issue being triaged.

## Step 4.3 -- Cross-CVE Overlap Detection

The Security Configuration in claude-md-security-config.md does **not** include the following optional fields:
- Upstream Affected Component custom field
- PS Component custom field
- Stream custom field

Per the skill specification: "If any of these fields are not configured, skip this step entirely."

**Result: Step 4.3 skipped** -- cross-CVE overlap detection requires the Upstream Affected Component, PS Component, and Stream custom fields to be configured in Security Configuration.

## Step 4 Summary

| Check | Result |
|-------|--------|
| Same-stream duplicates (4.1) | None found |
| Cross-stream siblings (4.2) | TC-8001 (2.2.x, In Progress) -- Related link already exists, skipped creation |
| Affects Versions overlap (4.2) | No overlap -- each issue owns its own stream's versions |
| Cross-CVE overlap (4.3) | Skipped -- required custom fields not configured |
