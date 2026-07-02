# Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check: TC-8006

## JQL Search for Sibling Issues

Query (proposed):
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

Results: 1 sibling found.

| Issue | Summary | Status | Stream Suffix | Affects Versions |
|-------|---------|--------|---------------|------------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | [rhtpa-2.2] | RHTPA 2.2.0, RHTPA 2.2.1 |

## Step 4.1 -- Same-Stream Duplicate Check

Current issue stream suffix: `[rhtpa-2.1]` (stream 2.1.x)

Sibling classification:
- TC-8001: stream suffix `[rhtpa-2.2]` (stream 2.2.x) -- **different stream**

Result: **No same-stream siblings found.** No duplicate closure needed.

## Step 4.2 -- Cross-Stream Coordination

TC-8001 is a **different-stream sibling** (companion tracker). PSIRT creates one issue per stream intentionally.

### Link Idempotency Check

Before creating a Related link, the skill checks the current issue's `issuelinks` array (already fetched in Step 1).

Existing links on TC-8006:
- Link ID 1990401: type.name = "Related", outwardIssue.key = "TC-8001"

Check criteria (all must match):
1. `type.name` is "Related" -- YES ("Related")
2. `inwardIssue.key` or `outwardIssue.key` matches the sibling key TC-8001 -- YES (`outwardIssue.key` = "TC-8001")

**A matching link already exists.** Link creation is skipped.

> Related link to TC-8001 already exists -- skipping

### Affects Versions Overlap Check

| Issue | Stream | Affects Versions |
|-------|--------|------------------|
| TC-8006 | 2.1.x | RHTPA 2.1.0 |
| TC-8001 | 2.2.x | RHTPA 2.2.0, RHTPA 2.2.1 |

No version overlap detected. Each issue carries only versions from its own stream. This is the correct state.

### Sibling Landscape

CVE-2026-31812 companion issues:

| Issue | Stream | Status | Affects Versions |
|-------|--------|--------|------------------|
| TC-8001 | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |
| TC-8006 (current) | 2.1.x | New | RHTPA 2.1.0 |

## Step 4.3 -- Cross-CVE Overlap Detection

The Upstream Affected Component custom field, PS Component custom field, and Stream custom field are **not configured** in Security Configuration.

Result: **Step 4.3 skipped entirely** (prerequisite fields not configured).

## Step 4.4 -- Preemptive Task Reconciliation

Query (proposed):
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```

This query would search for preemptive remediation tasks matching CVE-2026-31812 for the 2.1.x stream. Since we are simulating and no preemptive tasks are assumed to exist, this step proceeds silently to Step 5.

Result: **No matching preemptive task found.** Proceeding to Step 5.
