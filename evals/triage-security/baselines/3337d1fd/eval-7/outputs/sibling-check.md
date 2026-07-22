# Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check

## JQL Search for Siblings

Query (simulated):
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

### Results

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|------------------|---------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

## Step 4.1 -- Same-Stream Duplicate Check

- TC-8006 stream suffix: `[rhtpa-2.1]` (stream 2.1.x)
- TC-8001 stream suffix: `[rhtpa-2.2]` (stream 2.2.x)
- Classification: **different-stream sibling** (cross-stream companion)
- No same-stream duplicates found.

## Step 4.2 -- Cross-Stream Coordination

TC-8001 is a companion tracker for the same CVE in a different stream. Per Step 4.2, before creating a "Related" link, the skill checks the current issue's existing `issuelinks` array (already fetched in Step 1).

### Existing Link Check

The `issuelinks` array on TC-8006 contains:

```
- type.name: "Related"
  outwardIssue.key: "TC-8001"
  link ID: 1990401
  direction: outward (TC-8006 -> TC-8001)
```

Check criteria (all must be satisfied):
1. `type.name` is `"Related"` -- **YES**
2. `inwardIssue.key` or `outwardIssue.key` matches the sibling key `TC-8001` -- **YES** (outwardIssue.key = TC-8001)

**Result: A matching link already exists. Skip link creation.**

Log message:
> "Related link to TC-8001 already exists -- skipping"

### Affects Versions Overlap Check

| Issue | Stream | Affects Versions |
|-------|--------|------------------|
| TC-8006 | 2.1.x | RHTPA 2.1.0 |
| TC-8001 | 2.2.x | RHTPA 2.2.0, RHTPA 2.2.1 |

No overlap detected. Each issue carries only versions from its own stream.

### Sibling Landscape

```
CVE-2026-31812 companion issues:

| Issue       | Stream | Status      | Affects Versions              |
|-------------|--------|-------------|-------------------------------|
| TC-8001     | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1     |
| TC-8006 <-  | 2.1.x  | New         | RHTPA 2.1.0                   |
```

Arrow indicates the current issue being triaged.

## Step 4.3 -- Cross-CVE Overlap Detection

The Upstream Affected Component custom field, PS Component custom field, and Stream custom field are **not configured** in the Security Configuration (claude-md-security-config.md does not include these optional fields). Per the skill instructions, Step 4.3 is **skipped entirely** when these fields are not configured.

## Step 4.4 -- Preemptive Task Reconciliation

Search for preemptive tasks (simulated):
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```

No matching preemptive tasks found for CVE-2026-31812 in the 2.1.x stream. Proceeding to Step 5.
