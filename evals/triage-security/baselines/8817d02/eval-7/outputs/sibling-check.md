# Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check for TC-8006

## Step 4 Overview

This step searches for sibling Vulnerability issues with the same CVE label (CVE-2026-31812) and classifies them as same-stream duplicates or cross-stream companions.

## JQL Search for Siblings

Simulated JQL query:
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

### Search Results

| Issue Key | Summary | Status | Stream Suffix | Affects Versions |
|-----------|---------|--------|---------------|------------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | [rhtpa-2.2] | RHTPA 2.2.0, RHTPA 2.2.1 |

**Result count**: 1 sibling found.

## Step 4.1 -- Same-Stream Duplicate Check

- TC-8006 stream suffix: `[rhtpa-2.1]` (stream 2.1.x)
- TC-8001 stream suffix: `[rhtpa-2.2]` (stream 2.2.x)

**Classification**: TC-8001 is a **different-stream sibling** (companion tracker), NOT a same-stream duplicate. The stream suffixes differ (`rhtpa-2.1` vs `rhtpa-2.2`).

No same-stream duplicates found. TC-8006 is not a duplicate.

## Step 4.2 -- Cross-Stream Coordination

TC-8001 is a different-stream sibling (companion tracker). Per Step 4.2, we must:

1. **Check for existing link** before creating one.
2. **Verify no Affects Versions overlap** between the two issues.
3. **Present the sibling landscape** to the engineer.

### 4.2.1 -- Existing Link Check

Per Step 4.2 instructions: "Check for existing link before creating one. Read the current issue's `issuelinks` array from the `jira.get_issue` response (already fetched in Step 1). Check if any existing link satisfies all of:
- `type.name` is `"Related"`
- `inwardIssue.key` or `outwardIssue.key` matches the sibling key"

**Inspection of TC-8006's existing issue links:**

TC-8006 already has the following link:
- **Link type**: Related
- **Direction**: outward (TC-8006 -> TC-8001)
- **Linked issue key**: TC-8001
- **Link ID**: 1990401

This link satisfies ALL conditions:
- `type.name` is `"Related"` -- YES
- `outwardIssue.key` matches the sibling key `TC-8001` -- YES

**Decision: Related link to TC-8001 already exists -- skipping link creation.**

No `jira.create_link` call is needed. The pre-existing link is sufficient.

### 4.2.2 -- Affects Versions Overlap Check

| Issue | Stream | Affects Versions |
|-------|--------|------------------|
| TC-8006 (current) | 2.1.x | RHTPA 2.1.0 |
| TC-8001 (sibling) | 2.2.x | RHTPA 2.2.0, RHTPA 2.2.1 |

**No Affects Versions overlap detected.** TC-8006 carries only 2.1.x versions and TC-8001 carries only 2.2.x versions. Each issue owns versions from its own stream exclusively.

Note: TC-8006's Affects Versions (RHTPA 2.1.0 only) may need correction in Step 3 -- the version impact analysis shows both RHTPA 2.1.0 and RHTPA 2.1.1 are affected. This is an Affects Versions correction issue (Step 3), not a cross-stream overlap issue.

### 4.2.3 -- Sibling Landscape

CVE-2026-31812 companion issues:

| Issue | Stream | Status | Affects Versions |
|-------|--------|--------|------------------|
| TC-8001 | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |
| TC-8006 (current) | 2.1.x | New | RHTPA 2.1.0 |

TC-8001 is already In Progress, meaning remediation for the 2.2.x stream is actively being worked. TC-8006 needs its own remediation for the 2.1.x stream.

## Step 4.3 -- Cross-CVE Overlap Detection

The project's CLAUDE.md Security Configuration does not include the required fields for cross-CVE overlap detection:
- Upstream Affected Component custom field: **not configured**
- PS Component custom field: **not configured**
- Stream custom field: **not configured**

Per the skill instructions: "If any of these fields are not configured, skip this step entirely."

**Step 4.3 skipped.**

## Step 4.4 -- Preemptive Task Reconciliation

Simulated JQL query for preemptive tasks:
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```

No preemptive tasks are indicated in the fixture data for this CVE and the 2.1.x stream. The sibling TC-8001 is In Progress on the 2.2.x stream but no preemptive tasks were created for the 2.1.x stream.

**No matching preemptive task found. Proceeding to Step 5.**
