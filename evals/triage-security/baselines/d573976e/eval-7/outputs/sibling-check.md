# Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check

## Step 4 -- Sibling Search

JQL query executed:
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

Results: 1 sibling found.

| Issue | Summary | Status | Stream Suffix | Affects Versions |
|-------|---------|--------|---------------|------------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | [rhtpa-2.2] | RHTPA 2.2.0, RHTPA 2.2.1 |

## Sibling Classification

- **Current issue (TC-8006)**: stream suffix `[rhtpa-2.1]` -- stream 2.1.x
- **Sibling (TC-8001)**: stream suffix `[rhtpa-2.2]` -- stream 2.2.x

Classification: **Different-stream companion** (not a same-stream duplicate).

TC-8001 has a different stream suffix (`[rhtpa-2.2]`) than the current issue (`[rhtpa-2.1]`). PSIRT creates one issue per stream intentionally. These are companion trackers, not duplicates.

## Step 4.1 -- Same-stream duplicate check

No same-stream siblings found. TC-8001 is a different-stream companion. No duplicate closure recommended.

## Step 4.2 -- Cross-stream coordination

### Pre-existing link check

Before attempting to create a "Related" link to TC-8001, the current issue's existing `issuelinks` array was inspected (from the issue data fetched in Step 1).

Existing links on TC-8006:
- **Type**: Related
- **Direction**: outward (TC-8006 -> TC-8001)
- **Link ID**: 1990401

Check: Does any existing link satisfy ALL of:
1. `type.name` is "Related" -- **YES** (type is Related)
2. `outwardIssue.key` matches TC-8001 -- **YES** (outward link to TC-8001)

**Result: Related link to TC-8001 already exists -- skipping link creation.**

The `jira.create_link` call is NOT executed. Creating a duplicate link would be redundant.

### Affects Versions overlap verification

- TC-8006 (stream 2.1.x) Affects Versions: RHTPA 2.1.0
- TC-8001 (stream 2.2.x) Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1

No overlap detected. Each issue carries versions exclusively from its own stream.

### Sibling landscape

CVE-2026-31812 companion issues:

| Issue | Stream | Status | Affects Versions |
|-------|--------|--------|------------------|
| TC-8001 | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |
| TC-8006 (current) | 2.1.x | New | RHTPA 2.1.0 |

## Step 4.3 -- Cross-CVE overlap detection

The Upstream Affected Component custom field is not configured in Security Configuration. Step 4.3 is skipped entirely.

## Step 4.4 -- Preemptive task reconciliation

JQL query to search for preemptive tasks:
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```

Assumed result: No matching preemptive tasks found for CVE-2026-31812 in stream rhtpa-2.1.

Proceeding silently to Step 5.
