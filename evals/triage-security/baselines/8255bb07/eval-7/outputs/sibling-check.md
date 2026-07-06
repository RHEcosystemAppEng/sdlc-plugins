# Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check

## Step 4 -- JQL Sibling Search

Search query (simulated):
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

### Results

One sibling issue found:

| Issue | Summary | Status | Stream Suffix | Affects Versions |
|-------|---------|--------|---------------|------------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | [rhtpa-2.2] | RHTPA 2.2.0, RHTPA 2.2.1 |

## Step 4.1 -- Same-Stream Duplicate Check

- Current issue TC-8006 stream suffix: `[rhtpa-2.1]` (stream 2.1.x)
- Sibling TC-8001 stream suffix: `[rhtpa-2.2]` (stream 2.2.x)

Classification: **Different-stream sibling** (companion tracker). TC-8001 is NOT a same-stream duplicate.

No same-stream duplicates found. Proceeding to Step 4.2.

## Step 4.2 -- Cross-Stream Coordination

TC-8001 is a different-stream companion issue. Per Step 4.2 procedure:

### 1. Check for existing link before creating

Reading TC-8006's `issuelinks` array (fetched in Step 1):

- Link ID 1990401: type.name = "Related", direction = outward, outwardIssue.key = "TC-8001"

**Match found.** An existing link satisfies all conditions:
- type.name is "Related" -- YES
- outwardIssue.key matches sibling key TC-8001 -- YES

**Decision: Related link to TC-8001 already exists -- skipping link creation.**

This is the idempotent check required by Step 4.2: "Check for existing link before creating one. Read the current issue's issuelinks array from the jira.get_issue response (already fetched in Step 1). Check if any existing link satisfies all of: type.name is 'Related', inwardIssue.key or outwardIssue.key matches the sibling key. If a matching link exists, skip link creation."

No `jira.create_link` call is made.

### 2. Affects Versions overlap check

- TC-8006 (stream 2.1.x): Affects Versions = [RHTPA 2.1.0]
- TC-8001 (stream 2.2.x): Affects Versions = [RHTPA 2.2.0, RHTPA 2.2.1]

No version overlap detected. Each issue carries only versions from its own stream.

### 3. Sibling Landscape

```
CVE-2026-31812 companion issues:

| Issue      | Stream | Status      | Affects Versions              |
|------------|--------|-------------|-------------------------------|
| TC-8001    | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1     |
| TC-8006 <- | 2.1.x  | New         | RHTPA 2.1.0                   |
```

The arrow `<-` indicates the current issue being triaged.

## Step 4.3 -- Cross-CVE Overlap Detection

The Upstream Affected Component custom field is NOT configured in Security Configuration. Step 4.3 is skipped entirely per the prerequisite check.

## Step 4.4 -- Preemptive Task Reconciliation

Search for preemptive tasks (simulated):
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```

No matching preemptive tasks found for CVE-2026-31812 in stream rhtpa-2.1. Proceeding to Step 5.
