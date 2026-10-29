# Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check

## Step 4 JQL Search

Simulated JQL query:

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

### Search Results

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|------------------|---------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

One sibling found. Classifying by stream scope:

- **TC-8006** stream suffix: `[rhtpa-2.1]` (stream 2.1.x)
- **TC-8001** stream suffix: `[rhtpa-2.2]` (stream 2.2.x)
- Classification: **Different-stream sibling** (companion tracker, not a duplicate)

## Step 4.1 -- Same-Stream Duplicate Check

No same-stream siblings found. TC-8001 is scoped to stream 2.2.x while TC-8006 is scoped to stream 2.1.x. These are different streams, so TC-8001 is not a duplicate.

Result: **No duplicates detected.** Proceed to Step 4.2.

## Step 4.2 -- Cross-Stream Coordination

TC-8001 is a different-stream sibling (companion tracker for the same CVE in a different stream). Per the skill procedure, before creating a Related link, the skill must check for an existing link.

### Existing Link Check

Inspecting TC-8006's `issuelinks` array (fetched in Step 1):

- Link ID: 1990401
- Link type name: `Related`
- Direction: outward (TC-8006 -> TC-8001)
- Target issue key: TC-8001

**Check criteria (all must be satisfied):**

1. `type.name` is `"Related"` -- YES (link type is Related)
2. `inwardIssue.key` or `outwardIssue.key` matches the sibling key (TC-8001) -- YES (outwardIssue.key = TC-8001)

**All criteria satisfied.** A matching Related link already exists.

### Link Creation Decision

> Related link to TC-8001 already exists -- skipping

Link creation is **skipped**. The pre-existing Related link (ID 1990401) satisfies the cross-stream coordination requirement. No Jira mutation is needed.

### Affects Versions Overlap Verification

Checking for version overlap between the two sibling issues:

| Issue | Stream | Affects Versions |
|-------|--------|------------------|
| TC-8006 | 2.1.x | RHTPA 2.1.0 |
| TC-8001 | 2.2.x | RHTPA 2.2.0, RHTPA 2.2.1 |

**No overlap detected.** Each issue carries only versions from its own stream. The version partitioning is correct.

### Sibling Landscape

```
CVE-2026-31812 companion issues:

| Issue       | Stream | Status      | Affects Versions              |
|-------------|--------|-------------|-------------------------------|
| TC-8001     | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1     |
| TC-8006 <-  | 2.1.x  | New         | RHTPA 2.1.0                   |
```

The arrow (`<-`) marks the current issue being triaged.

## Step 4.3 -- Cross-CVE Overlap Detection

**Skipped.** The Upstream Affected Component custom field, PS Component custom field, and Stream custom field are not configured in the project's Security Configuration. Per the skill procedure, Step 4.3 is skipped entirely when these fields are not configured.

## Step 4.4 -- Preemptive Task Reconciliation

Simulated JQL query:

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```

Assumed result: **No matching preemptive tasks found** for CVE-2026-31812 in stream 2.1.x.

Result: Proceed to Step 5. No preemptive task reconciliation needed.
