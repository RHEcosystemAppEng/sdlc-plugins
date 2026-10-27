# Step 4 -- Sibling and Link Analysis: TC-8006

## Step 4 Overview

Step 4 searches for sibling Vulnerability issues with the same CVE label (CVE-2026-31812) and classifies them as same-stream duplicates or different-stream companions.

### JQL Search

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

**Result**: 1 sibling found.

| Issue | Summary | Status | Stream Suffix | Affects Versions |
|-------|---------|--------|---------------|------------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | [rhtpa-2.2] | RHTPA 2.2.0, RHTPA 2.2.1 |

## Step 4.1 -- Same-Stream Duplicate Check

TC-8001 has stream suffix `[rhtpa-2.2]`, which differs from TC-8006's stream suffix `[rhtpa-2.1]`. This is a **different-stream sibling** (companion tracker), not a same-stream duplicate.

**Result**: No same-stream duplicates found. Proceeding to Step 4.2.

## Step 4.2 -- Cross-Stream Coordination

TC-8001 is a different-stream companion for CVE-2026-31812. PSIRT creates one issue per stream intentionally. Per the Step 4.2 procedure, before creating a Related link, the existing `issuelinks` on TC-8006 must be checked.

### Existing Link Check

Inspecting TC-8006's `issuelinks` array (fetched in Step 1):

- **Link found**: Related link to TC-8001
  - Link ID: 1990401
  - Type: Related
  - Direction: outward (TC-8006 -> TC-8001)

The existing link satisfies all conditions:
1. `type.name` is "Related" -- YES
2. `outwardIssue.key` matches the sibling key (TC-8001) -- YES

**Decision**: Related link to TC-8001 already exists -- skipping link creation.

> Related link to TC-8001 already exists -- skipping

### Affects Versions Overlap Check

| Issue | Stream | Affects Versions |
|-------|--------|------------------|
| TC-8006 | 2.1.x | RHTPA 2.1.0 |
| TC-8001 | 2.2.x | RHTPA 2.2.0, RHTPA 2.2.1 |

No version overlap detected. Each issue carries only versions from its own stream.

### Sibling Landscape

```
CVE-2026-31812 companion issues:

| Issue      | Stream | Status      | Affects Versions              |
|------------|--------|-------------|-------------------------------|
| TC-8001    | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1     |
| TC-8006 <- | 2.1.x  | New         | RHTPA 2.1.0                   |
```

The arrow `<-` marks the current issue being triaged.

## Step 4.3 -- Cross-CVE Overlap Detection

The Upstream Affected Component custom field is not configured in the project's Security Configuration. Step 4.3 is skipped entirely per the prerequisite.

## Step 4.4 -- Preemptive Task Reconciliation

No preemptive tasks were searched for in this eval (Step 4.4 would search for Tasks with the `security-preemptive` label matching CVE-2026-31812 and stream rhtpa-2.1). No preemptive task reconciliation is needed based on the available data.
