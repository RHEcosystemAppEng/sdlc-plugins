# Step 4 -- Duplicate, Sibling, and Overlap Check for TC-8006

## Step 4 -- Sibling Search

JQL query (simulated):
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

### Results

One sibling found:

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|------------------|---------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

### Sibling Classification

- **TC-8006** stream suffix: `[rhtpa-2.1]` (stream 2.1.x)
- **TC-8001** stream suffix: `[rhtpa-2.2]` (stream 2.2.x)

TC-8001 has a **different** stream suffix from TC-8006. This is a **different-stream sibling** -- a companion tracker, NOT a duplicate. PSIRT creates one issue per stream intentionally.

## Step 4.1 -- Same-stream Duplicate Check

No same-stream siblings found. TC-8001 is scoped to stream 2.2.x, while TC-8006 is scoped to stream 2.1.x. No duplicate closure is needed.

## Step 4.2 -- Cross-stream Coordination

TC-8001 is a different-stream companion tracker. Per the Step 4.2 procedure:

### 4.2.1 -- Check for Existing Link Before Creating One

Read the current issue's (TC-8006) `issuelinks` array from the issue data (already fetched in Step 1). The existing links are:

- Link ID: 1990401
  - Type: **Related**
  - Direction: outward (TC-8006 --> TC-8001)
  - outwardIssue.key: **TC-8001**

Check whether any existing link satisfies ALL of:
1. `type.name` is `"Related"` -- **YES** (type is Related)
2. `inwardIssue.key` or `outwardIssue.key` matches the sibling key TC-8001 -- **YES** (outwardIssue.key is TC-8001)

**Result: A matching link exists.**

Action: **Skip link creation** and log:

> "Related link to TC-8001 already exists -- skipping"

No `jira.create_link` call is made. The pre-existing Related link (ID 1990401) already satisfies the cross-stream coordination requirement. This is the idempotent behavior specified by Step 4.2: always check existing links before creating new ones to avoid duplicates.

### 4.2.2 -- Verify No Affects Versions Overlap

| Issue | Stream | Affects Versions |
|-------|--------|------------------|
| TC-8006 | 2.1.x | RHTPA 2.1.0 |
| TC-8001 | 2.2.x | RHTPA 2.2.0, RHTPA 2.2.1 |

Each issue carries only versions from its own stream. **No overlap detected.** No action required.

### 4.2.3 -- Sibling Landscape

CVE-2026-31812 companion issues:

| Issue | Stream | Status | Affects Versions |
|-------|--------|--------|------------------|
| TC-8001 | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |
| TC-8006 (current) | 2.1.x | New | RHTPA 2.1.0 |

The arrow indicates the current issue being triaged.

## Step 4.3 -- Cross-CVE Overlap Detection

The Upstream Affected Component custom field is not configured in the Security Configuration (claude-md-security-config.md does not include it). Per the skill specification, Step 4.3 is **skipped entirely** when this field is not configured.

## Step 4.4 -- Preemptive Task Reconciliation

No preemptive task search was specified in the eval inputs. Proceeding to Step 5.
