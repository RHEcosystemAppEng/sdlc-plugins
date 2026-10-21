# Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check

## 4.0 -- JQL Sibling Search

JQL query (simulated):
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

**Result**: 1 sibling found.

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|-----------------|---------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

## 4.1 -- Same-Stream Duplicate Check

- **TC-8006 stream suffix**: [rhtpa-2.1] (stream 2.1.x)
- **TC-8001 stream suffix**: [rhtpa-2.2] (stream 2.2.x)

**Classification**: Different-stream sibling (companion tracker). TC-8001 tracks the same CVE for a different product version stream. This is NOT a duplicate -- PSIRT creates one issue per stream intentionally.

**Result**: No same-stream duplicates found. Proceeding to Step 4.2.

## 4.2 -- Cross-Stream Coordination

TC-8001 is a different-stream companion tracker. Per the Step 4.2 procedure:

### Link Idempotency Check

Before creating a Related link to TC-8001, the skill checks the current issue's `issuelinks` array (already fetched in Step 1).

**Existing links on TC-8006:**
- Related link (outward): TC-8006 -> TC-8001 (link ID: 1990401)

**Check criteria** (all must be satisfied):
1. `type.name` is "Related" -- YES (link type is Related)
2. `inwardIssue.key` or `outwardIssue.key` matches the sibling key (TC-8001) -- YES (outwardIssue.key = TC-8001)

**All criteria satisfied.** A matching Related link to TC-8001 already exists.

**Action**: Skip link creation. Log:
> "Related link to TC-8001 already exists -- skipping"

No Jira `create_link` call is made. The pre-existing link is sufficient for cross-stream coordination.

### Affects Versions Overlap Check

- **TC-8006 Affects Versions**: RHTPA 2.1.0 (stream 2.1.x)
- **TC-8001 Affects Versions**: RHTPA 2.2.0, RHTPA 2.2.1 (stream 2.2.x)

**Result**: No version overlap detected. Each issue carries only versions from its own stream.

### Sibling Landscape Presentation

```
CVE-2026-31812 companion issues:

| Issue      | Stream | Status      | Affects Versions             |
|------------|--------|-------------|------------------------------|
| TC-8001    | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1    |
| TC-8006 <- | 2.1.x  | New         | RHTPA 2.1.0                  |
```

The arrow (<-) marks the current issue being triaged.

## 4.3 -- Cross-CVE Overlap Detection

**Prerequisite check**: The project's Security Configuration does NOT include Upstream Affected Component custom field, PS Component custom field, or Stream custom field configuration.

**Result**: Step 4.3 is skipped entirely (required custom fields not configured).

## 4.4 -- Preemptive Task Reconciliation

JQL search (simulated):
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```

**Result**: No matching preemptive tasks found for CVE-2026-31812 in stream 2.1.x.

Proceeding to Step 5 (Version Lifecycle Check).
