# Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check

## Step 4 -- JQL Sibling Search

JQL query (simulated):
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

### Results

One sibling found:

| Issue | Summary | Status | Stream Suffix | Affects Versions |
|-------|---------|--------|---------------|------------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | [rhtpa-2.2] | RHTPA 2.2.0, RHTPA 2.2.1 |

### Classification

- TC-8006 stream suffix: `[rhtpa-2.1]` (stream 2.1.x)
- TC-8001 stream suffix: `[rhtpa-2.2]` (stream 2.2.x)
- Classification: **Different-stream sibling** (companion tracker)

TC-8001 is NOT a same-stream duplicate. It is a cross-stream companion issue created by PSIRT to track the same CVE in a different product version stream.

## Step 4.1 -- Same-Stream Duplicate Check

No same-stream siblings found. TC-8001 has a different stream suffix (`[rhtpa-2.2]` vs `[rhtpa-2.1]`). No duplicate closure needed.

## Step 4.2 -- Cross-Stream Coordination

TC-8001 is a different-stream sibling. Per Step 4.2, before creating a "Related" link, check the current issue's existing `issuelinks` array for a matching link.

### Pre-existing Link Check

The issue's `issuelinks` (fetched in Step 1) contains:

- Link type: **Related**
- Direction: outward (TC-8006 -> TC-8001)
- Link ID: 1990401
- Outward issue key: **TC-8001**

Check criteria:
1. `type.name` is "Related"? **Yes**
2. `outwardIssue.key` matches sibling key TC-8001? **Yes**

**Result: A matching Related link to TC-8001 already exists.**

Action: **Skip link creation.** Log:
> "Related link to TC-8001 already exists -- skipping"

### Affects Versions Overlap Check

- TC-8006 Affects Versions: RHTPA 2.1.0 (stream 2.1.x)
- TC-8001 Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1 (stream 2.2.x)

No overlapping versions detected. Each issue carries only versions from its own stream.

### Sibling Landscape

CVE-2026-31812 companion issues:

| Issue | Stream | Status | Affects Versions |
|-------|--------|--------|------------------|
| TC-8001 | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |
| TC-8006 (current) | 2.1.x | New | RHTPA 2.1.0 |

## Step 4.3 -- Cross-CVE Overlap Detection

Skipped. The Upstream Affected Component custom field, PS Component custom field, and Stream custom field are not configured in Security Configuration. Per the skill definition, Step 4.3 is skipped entirely when these fields are not configured.

## Step 4.4 -- Preemptive Task Reconciliation

No preemptive tasks found matching CVE-2026-31812 for stream rhtpa-2.1 (simulated: JQL search for `labels = 'security-preemptive' AND labels = 'CVE-2026-31812'` returned no results). Proceeding to Step 5.
