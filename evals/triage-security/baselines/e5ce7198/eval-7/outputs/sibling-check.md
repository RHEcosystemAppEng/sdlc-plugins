# Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check for TC-8006

## Step 4 Overview

This step searches for sibling Vulnerability issues with the same CVE label (CVE-2026-31812) and classifies them as same-stream duplicates or cross-stream companions.

## JQL Search Executed (simulated)

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

### Search Results

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|------------------|---------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

One sibling found: TC-8001.

## Step 4.1 -- Same-Stream Duplicate Check

- TC-8006 stream suffix: `[rhtpa-2.1]` (stream 2.1.x)
- TC-8001 stream suffix: `[rhtpa-2.2]` (stream 2.2.x)
- Classification: **Different-stream sibling** (not a same-stream duplicate)

No same-stream duplicates detected. Proceeding to Step 4.2.

## Step 4.2 -- Cross-Stream Coordination

TC-8001 is a **companion tracker** for the same CVE in a different stream (2.2.x). PSIRT creates one issue per stream intentionally; these are not duplicates.

### Pre-Existing Link Check

Per Step 4.2 procedure: before creating a "Related" link, check the current issue's `issuelinks` array (already fetched in Step 1) for an existing link that satisfies all of:
- `type.name` is "Related"
- `inwardIssue.key` or `outwardIssue.key` matches the sibling key (TC-8001)

**Inspection of TC-8006 existing issue links:**

| Link Type | Direction | Linked Issue | Link ID |
|-----------|-----------|--------------|---------|
| Related | outward (TC-8006 -> TC-8001) | TC-8001 | 1990401 |

**Result:** A matching "Related" link to TC-8001 **already exists** (Link ID 1990401, direction: outward).

**Action taken:** Link creation **skipped** -- the Related link to TC-8001 already exists.

> "Related link to TC-8001 already exists -- skipping"

This is the idempotent behavior specified by Step 4.2: "If a matching link exists, skip link creation and log: 'Related link to [sibling-key] already exists -- skipping'."

### Affects Versions Overlap Check

- TC-8006 Affects Versions: RHTPA 2.1.0 (stream 2.1.x)
- TC-8001 Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1 (stream 2.2.x)
- **No overlap detected.** Each issue carries only versions from its own stream.

### Sibling Landscape

```
CVE-2026-31812 companion issues:

| Issue      | Stream | Status      | Affects Versions              |
|------------|--------|-------------|-------------------------------|
| TC-8001    | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1     |
| TC-8006 <- | 2.1.x  | New         | RHTPA 2.1.0                   |
```

The arrow (<-) indicates the current issue being triaged.

## Step 4.3 -- Cross-CVE Overlap Detection

The CLAUDE.md Security Configuration does not include an Upstream Affected Component custom field, PS Component custom field, or Stream custom field. Per the skill procedure: "If any of these fields are not configured, skip this step entirely."

**Step 4.3 skipped.**

## Step 4.4 -- Preemptive Task Reconciliation

A JQL search would be performed (simulated):

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```

No matching preemptive tasks were found for CVE-2026-31812 in the 2.1.x stream.

**Proceeding to Step 5.**

## Summary of Step 4

| Sub-step | Result |
|----------|--------|
| 4.1 Same-stream duplicates | None found |
| 4.2 Cross-stream coordination | TC-8001 (stream 2.2.x) identified as companion; pre-existing Related link found -- link creation skipped (idempotent) |
| 4.3 Cross-CVE overlap | Skipped (custom fields not configured) |
| 4.4 Preemptive task reconciliation | No preemptive tasks found |
