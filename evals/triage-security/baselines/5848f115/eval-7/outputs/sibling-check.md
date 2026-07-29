# Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check: TC-8006

## Step 4 -- JQL Sibling Search

**Query** (simulated):
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

**Results**: 1 sibling found.

| Issue | Summary | Status | Stream Suffix | Affects Versions |
|-------|---------|--------|---------------|------------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | [rhtpa-2.2] | RHTPA 2.2.0, RHTPA 2.2.1 |

## Sibling Classification

- **TC-8006** stream suffix: `[rhtpa-2.1]` (stream 2.1.x)
- **TC-8001** stream suffix: `[rhtpa-2.2]` (stream 2.2.x)
- Classification: **Different-stream sibling** (cross-stream companion, NOT a duplicate)

PSIRT creates one Vulnerability issue per stream intentionally. TC-8001 is a companion tracker for the same CVE in a different stream.

## Step 4.1 -- Same-Stream Duplicate Check

No same-stream siblings found. TC-8001 is a different-stream companion (2.2.x vs 2.1.x). No duplicate handling required.

## Step 4.2 -- Cross-Stream Coordination

### Link Check (Idempotent)

Per SKILL.md Step 4.2, before creating a "Related" link, check the current issue's `issuelinks` array for an existing link.

**Existing links on TC-8006** (from Step 1 data extraction):
- Link ID: 1990401
- Type: **Related**
- Direction: outward (TC-8006 -> TC-8001)

**Check**: Does any existing link satisfy ALL of:
1. `type.name` is `"Related"` -- YES (type is Related)
2. `inwardIssue.key` or `outwardIssue.key` matches `TC-8001` -- YES (outwardIssue.key is TC-8001)

**Result**: All conditions satisfied. A matching "Related" link to TC-8001 already exists.

**Action**: Skip link creation.

> "Related link to TC-8001 already exists -- skipping"

### Affects Versions Overlap Check

| Issue | Stream | Affects Versions |
|-------|--------|------------------|
| TC-8006 | 2.1.x | RHTPA 2.1.0 |
| TC-8001 | 2.2.x | RHTPA 2.2.0, RHTPA 2.2.1 |

**Result**: No version overlap detected. Each issue carries only versions from its own stream. This is the correct state.

### Sibling Landscape

CVE-2026-31812 companion issues:

| Issue | Stream | Status | Affects Versions |
|-------|--------|--------|------------------|
| TC-8001 | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |
| TC-8006 (current) | 2.1.x | New | RHTPA 2.1.0 |

## Step 4.3 -- Cross-CVE Overlap Detection

The Upstream Affected Component custom field, PS Component custom field, and Stream custom field are **not configured** in the project's Security Configuration. Per SKILL.md, this step is skipped entirely when these fields are not configured.

**Result**: Skipped.

## Step 4.4 -- Preemptive Task Reconciliation

No preemptive tasks searched for in this simulated run. This step would search for existing `security-preemptive` labeled tasks matching CVE-2026-31812 for stream 2.1.x. In the absence of external Jira access, no preemptive tasks are assumed to exist. Proceed to Step 5.
