# Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check

## Step 4 JQL Search

Simulated JQL query:
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

### Search Results

One sibling issue found:

| Issue | Summary | Stream Suffix | Status | Affects Versions |
|-------|---------|---------------|--------|------------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | [rhtpa-2.2] | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |

## Step 4.1 -- Same-Stream Duplicate Check

- TC-8006 stream suffix: `[rhtpa-2.1]` (stream 2.1.x)
- TC-8001 stream suffix: `[rhtpa-2.2]` (stream 2.2.x)

**Result**: TC-8001 is a **different-stream sibling**, NOT a same-stream duplicate. The two issues are companion trackers -- PSIRT created one issue per stream intentionally.

No same-stream duplicates found. Proceeding to Step 4.2.

## Step 4.2 -- Cross-Stream Coordination

TC-8001 is a cross-stream companion issue for the same CVE (CVE-2026-31812), tracking stream 2.2.x while TC-8006 tracks stream 2.1.x.

### Link Idempotency Check

Before creating a Related link, Step 4.2 requires checking the current issue's `issuelinks` array for an existing link that satisfies all of:
- `type.name` is "Related"
- `inwardIssue.key` or `outwardIssue.key` matches the sibling key (TC-8001)

**Existing links on TC-8006:**
- Related link to TC-8001 (link ID: 1990401, direction: outward, TC-8006 -> TC-8001)

**Check result**: A matching link exists -- type is "Related" and `outwardIssue.key` is TC-8001.

**Action**: **Skip link creation.**

> "Related link to TC-8001 already exists -- skipping"

This is the idempotent behavior specified in Step 4.2: the skill checks for an existing link before attempting to create one. Since TC-8006 already has a Related link to TC-8001, no duplicate link is created.

### Affects Versions Overlap Check

- TC-8006 Affects Versions: RHTPA 2.1.0
- TC-8001 Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1

**Result**: No overlap detected. Each issue carries only versions from its own stream. No version overlap warning needed.

### Sibling Landscape

CVE-2026-31812 companion issues:

| Issue | Stream | Status | Affects Versions |
|-------|--------|--------|------------------|
| TC-8001 | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |
| TC-8006 (current) | 2.1.x | New | RHTPA 2.1.0 |

## Step 4.3 -- Cross-CVE Overlap Detection

The Upstream Affected Component custom field is NOT configured in the project's Security Configuration (claude-md-security-config.md does not include it). Per the skill instructions, Step 4.3 is skipped entirely when this field is not configured.

**Result**: Step 4.3 skipped.

## Step 4.4 -- Preemptive Task Reconciliation

Simulated JQL query:
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```

No preemptive tasks found for CVE-2026-31812 in stream 2.1.x.

**Result**: No reconciliation needed. Proceed to Step 5.
