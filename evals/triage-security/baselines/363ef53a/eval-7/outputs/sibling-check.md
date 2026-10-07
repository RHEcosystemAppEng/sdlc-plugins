# Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check for TC-8006

## Step 4 JQL Search

Query (simulated):
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

Results: **1 sibling found**

| Issue | Summary | Stream Suffix | Status | Affects Versions |
|-------|---------|---------------|--------|-----------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | [rhtpa-2.2] | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |

## Step 4.1 -- Same-Stream Duplicate Check

TC-8001 has stream suffix `[rhtpa-2.2]` (2.2.x stream). TC-8006 has stream suffix `[rhtpa-2.1]` (2.1.x stream). These are **different streams**.

Classification: **Different-stream sibling (companion tracker)** -- not a duplicate.

No same-stream duplicates found. Step 4.1 does not apply.

## Step 4.2 -- Cross-Stream Coordination

TC-8001 is a different-stream sibling (companion tracker for 2.2.x). Per the skill procedure, a "Related" link should exist between the current issue and each different-stream sibling.

### Link Idempotency Check

Before creating a link, Step 4.2 requires checking the current issue's `issuelinks` array for an existing link that satisfies all of:
- `type.name` is `"Related"`
- `inwardIssue.key` or `outwardIssue.key` matches the sibling key (TC-8001)

**Existing links on TC-8006** (from Step 1 data extraction):

| Link ID | Type | Direction | Target |
|---------|------|-----------|--------|
| 1990401 | Related | outward (TC-8006 -> TC-8001) | TC-8001 |

**Check result**: A link with `type.name = "Related"` and `outwardIssue.key = "TC-8001"` already exists (Link ID 1990401).

**Action**: Skip link creation.

Log message:
> "Related link to TC-8001 already exists -- skipping"

### Affects Versions Overlap Check

TC-8006 Affects Versions (after Step 3 correction for 2.1.x scope): RHTPA 2.1.0, RHTPA 2.1.1
TC-8001 Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1

No version overlap detected -- each issue carries only versions from its own stream. This is correct behavior.

### Sibling Landscape

```
CVE-2026-31812 companion issues:

| Issue      | Stream | Status      | Affects Versions              |
|------------|--------|-------------|-------------------------------|
| TC-8001    | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1     |
| TC-8006 <- | 2.1.x  | New         | RHTPA 2.1.0                   |
```

Arrow indicates the current issue being triaged.

## Step 4.3 -- Cross-CVE Overlap Detection

The Upstream Affected Component custom field is not configured in the Security Configuration (no `customfield_XXXXX` entry for Upstream Affected Component). Per the skill procedure:

> "If any of these fields are not configured, skip this step entirely."

**Action**: Step 4.3 skipped.

## Step 4.4 -- Preemptive Task Reconciliation

Search for preemptive tasks matching CVE-2026-31812 for the 2.1.x stream (simulated):

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```

**Results**: No matching preemptive tasks found for this CVE and stream.

**Action**: Proceed to Step 5.
