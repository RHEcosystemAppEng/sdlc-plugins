# Step 4 -- Sibling and Link Analysis: TC-8006

## Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check

### JQL Search for Siblings

Query (simulated):
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

Results: **1 sibling found**

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|------------------|---------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

### Sibling Classification

- **TC-8006** stream suffix: `[rhtpa-2.1]` (stream 2.1.x)
- **TC-8001** stream suffix: `[rhtpa-2.2]` (stream 2.2.x)
- Classification: **Different-stream companion** (NOT a same-stream duplicate)

TC-8001 is a companion tracker for the same CVE in a different version stream. PSIRT creates one Vulnerability issue per stream intentionally. This is expected cross-stream tracking.

### Step 4.1 -- Same-Stream Duplicate Check

No same-stream siblings found. TC-8001 has stream suffix `[rhtpa-2.2]` which differs from TC-8006's `[rhtpa-2.1]`. Step 4.1 does not apply.

### Step 4.2 -- Cross-Stream Coordination

**Link idempotency check:**

Before creating a Related link to TC-8001, check the existing `issuelinks` array on TC-8006 (fetched in Step 1).

Existing links on TC-8006:
- Link ID 1990401: type = "Related", direction = outward, outwardIssue.key = "TC-8001"

Check criteria:
1. `type.name` is "Related" -- YES (matches)
2. `outwardIssue.key` matches sibling key TC-8001 -- YES (matches)

**Result: A matching Related link to TC-8001 already exists.**

> Related link to TC-8001 already exists -- skipping

Link creation is **skipped** because the pre-existing link satisfies all matching criteria. This is the idempotent behavior specified in Step 4.2: "If a matching link exists, skip link creation and log."

**Affects Versions overlap check:**

| Issue | Stream | Affects Versions |
|-------|--------|------------------|
| TC-8006 | 2.1.x | RHTPA 2.1.0 |
| TC-8001 | 2.2.x | RHTPA 2.2.0, RHTPA 2.2.1 |

No overlap detected. Each issue carries versions exclusively from its own stream. RHTPA 2.1.0 belongs to the 2.1.x stream, while RHTPA 2.2.0 and RHTPA 2.2.1 belong to the 2.2.x stream.

### Sibling Landscape

CVE-2026-31812 companion issues:

| Issue | Stream | Status | Affects Versions |
|-------|--------|--------|------------------|
| TC-8001 | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |
| TC-8006 (current) | 2.1.x | New | RHTPA 2.1.0 |

The sibling landscape is presented to the engineer for awareness. TC-8001 is already In Progress in stream 2.2.x, indicating active remediation work on the companion stream.
