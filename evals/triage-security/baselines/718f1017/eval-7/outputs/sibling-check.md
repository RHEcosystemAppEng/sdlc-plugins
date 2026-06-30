# Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check for TC-8006

## Step 4 Overview

Step 4 searches for sibling Vulnerability issues with the same CVE label to detect duplicates, coordinate cross-stream companion issues, check for cross-CVE overlap, and reconcile preemptive tasks.

## JQL Search for Siblings

Simulated JQL query:
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

### Results: 1 sibling found

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|------------------|---------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

## Step 4.1 -- Same-Stream Duplicate Check

- TC-8006 stream suffix: `[rhtpa-2.1]` (stream 2.1.x)
- TC-8001 stream suffix: `[rhtpa-2.2]` (stream 2.2.x)
- Classification: **Different-stream sibling** (not a same-stream duplicate)

TC-8001 is a **companion tracker** for the same CVE in a different stream. PSIRT creates one issue per stream intentionally. This is NOT a duplicate.

No same-stream duplicates found. No closure recommendation.

## Step 4.2 -- Cross-Stream Coordination

TC-8001 is a different-stream sibling (companion tracker for stream 2.2.x).

### Link Check (Idempotent)

Per the methodology (Step 4.2), before creating a "Related" link, the skill checks the current issue's `issuelinks` array (already fetched in Step 1) for an existing link that satisfies ALL of:
1. `type.name` is `"Related"`
2. `inwardIssue.key` or `outwardIssue.key` matches the sibling key (TC-8001)

**Existing links on TC-8006:**
- Link ID: 1990401
  - Type: **Related**
  - Direction: outward (TC-8006 -> TC-8001)
  - outwardIssue.key: **TC-8001**

**Result:** A matching "Related" link to TC-8001 already exists on TC-8006. Both conditions are satisfied:
- type.name is "Related" -- YES
- outwardIssue.key matches TC-8001 -- YES

**Action:** Skip link creation. Log:
> "Related link to TC-8001 already exists -- skipping"

No new link is created. The existing link is sufficient for cross-stream coordination.

### Affects Versions Overlap Check

- TC-8006 Affects Versions: RHTPA 2.1.0 (stream 2.1.x)
- TC-8001 Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1 (stream 2.2.x)
- Overlap: **None** -- each issue carries only versions from its own stream

### Sibling Landscape

CVE-2026-31812 companion issues:

| Issue | Stream | Status | Affects Versions |
|-------|--------|--------|------------------|
| TC-8001 | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |
| TC-8006 (current) | 2.1.x | New | RHTPA 2.1.0 |

## Step 4.3 -- Cross-CVE Overlap Detection

The Security Configuration does not include Upstream Affected Component custom field, PS Component custom field, or Stream custom field. Per the methodology, Step 4.3 is skipped entirely when these fields are not configured.

**Action:** Skipped.

## Step 4.4 -- Preemptive Task Reconciliation

Simulated JQL query for preemptive tasks:
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```

No matching preemptive tasks found for CVE-2026-31812 in the 2.1.x stream.

**Action:** Proceed to Step 5.
