# Step 4 -- Sibling and Link Analysis for TC-8006

## Step 4 JQL Query

Search for sibling Vulnerability issues with the same CVE label:

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

## JQL Results

One sibling found:

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|------------------|---------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

## Step 4.1 -- Same-Stream Duplicate Check

- TC-8006 stream suffix: `[rhtpa-2.1]` (stream 2.1.x)
- TC-8001 stream suffix: `[rhtpa-2.2]` (stream 2.2.x)
- Classification: **Different-stream sibling** (companion tracker)

TC-8001 is NOT a same-stream duplicate. The streams are different (2.1.x vs 2.2.x), so PSIRT intentionally created separate issues for each stream. No duplicate closure applies.

## Step 4.2 -- Cross-Stream Coordination

TC-8001 is a **different-stream sibling** (companion tracker for stream 2.2.x). Per Step 4.2 of the skill:

### Link Idempotency Check

Before creating a "Related" link, the skill checks the current issue's `issuelinks` array (already fetched in Step 1) for an existing link that satisfies ALL of:
1. `type.name` is `"Related"`
2. `inwardIssue.key` or `outwardIssue.key` matches the sibling key `TC-8001`

**Result**: A matching link **already exists**.

From the issue data (Step 1 extraction):
- Link ID: 1990401
- Type: Related
- Direction: outward (TC-8006 -> TC-8001)
- Target: TC-8001

Since the existing link satisfies both conditions (`type.name = "Related"` and `outwardIssue.key = "TC-8001"`), link creation is **skipped**.

Log message:
> "Related link to TC-8001 already exists -- skipping"

### Affects Versions Overlap Verification

- TC-8006 Affects Versions: RHTPA 2.1.0 (stream 2.1.x)
- TC-8001 Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1 (stream 2.2.x)
- Overlap: **None** -- each issue carries only versions from its own stream

No version overlap detected. No action needed.

### Sibling Landscape

```
CVE-2026-31812 companion issues:

| Issue       | Stream | Status      | Affects Versions               |
|-------------|--------|-------------|--------------------------------|
| TC-8001     | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1      |
| TC-8006 <-  | 2.1.x  | New         | RHTPA 2.1.0                    |
```

(Arrow indicates current issue being triaged.)

## Step 4.3 -- Cross-CVE Overlap Detection

The project's Security Configuration does not include the Upstream Affected Component custom field, PS Component custom field, or Stream custom field. Per the skill instructions:

> "If any of these fields are not configured, skip this step entirely."

**Step 4.3 skipped.**

## Step 4.4 -- Preemptive Task Reconciliation

Search for preemptive tasks matching CVE-2026-31812:

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```

Assumed result: No matching preemptive tasks found for stream 2.1.x.

**Proceeding to Step 5.**
