# Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check for TC-8006

## Step 4 JQL Search

Search query (simulated):
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

### JQL Results

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|-----------------|---------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

## Sibling Classification

- TC-8006 stream suffix: `[rhtpa-2.1]` (stream 2.1.x)
- TC-8001 stream suffix: `[rhtpa-2.2]` (stream 2.2.x)
- Classification: **Different-stream sibling** (cross-stream companion tracker)

TC-8001 is NOT a duplicate. PSIRT creates one Vulnerability issue per stream intentionally. TC-8001 tracks the same CVE for the 2.2.x stream while TC-8006 tracks it for the 2.1.x stream.

## Step 4.1 -- Same-Stream Duplicate Check

No same-stream siblings found. TC-8001 is scoped to a different stream (2.2.x vs 2.1.x). No duplicate closure recommended.

## Step 4.2 -- Cross-Stream Coordination

### Pre-existing Link Check (Idempotent Linking)

Per Step 4.2 procedure, before creating a Related link to a different-stream sibling, the skill checks the current issue's `issuelinks` array for an existing link that satisfies ALL of:
1. `type.name` is `"Related"`
2. `inwardIssue.key` or `outwardIssue.key` matches the sibling key (TC-8001)

**Existing links on TC-8006:**

| Link ID | Type | Direction | Linked Issue |
|---------|------|-----------|-------------|
| 1990401 | Related | outward (TC-8006 -> TC-8001) | TC-8001 |

**Check result:** A link matching ALL criteria was found:
- `type.name` = "Related" -- matches
- `outwardIssue.key` = TC-8001 -- matches the sibling key

**Action:** Related link to TC-8001 already exists -- skipping link creation.

This is the idempotent behavior specified by Step 4.2: "If a matching link exists, skip link creation and log: 'Related link to [sibling-key] already exists -- skipping'"

### Affects Versions Overlap Verification

Per Step 4.2 procedure, verify no Affects Versions overlap between sibling issues (each issue should only carry versions from its own stream):

| Issue | Stream | Affects Versions |
|-------|--------|-----------------|
| TC-8006 | 2.1.x | RHTPA 2.1.0 |
| TC-8001 | 2.2.x | RHTPA 2.2.0, RHTPA 2.2.1 |

**Result:** No overlap detected. TC-8006 carries only 2.1.x versions and TC-8001 carries only 2.2.x versions. Each issue correctly owns versions from its own stream.

### Sibling Landscape

CVE-2026-31812 companion issues:

| Issue | Stream | Status | Affects Versions |
|-------|--------|--------|-----------------|
| TC-8001 | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |
| TC-8006 (current) | 2.1.x | New | RHTPA 2.1.0 |

## Step 4.3 -- Cross-CVE Overlap Detection

The Security Configuration does not include an Upstream Affected Component custom field, PS Component custom field, or Stream custom field. Per Step 4.3 prerequisite: "If any of these fields are not configured, skip this step entirely."

**Action:** Step 4.3 skipped.

## Step 4.4 -- Preemptive Task Reconciliation

A search for preemptive tasks matching CVE-2026-31812 with the `security-preemptive` label would be performed (simulated). Assuming no matching preemptive tasks are found for stream 2.1.x.

**Action:** No matching preemptive task found. Proceeding to Step 5.
