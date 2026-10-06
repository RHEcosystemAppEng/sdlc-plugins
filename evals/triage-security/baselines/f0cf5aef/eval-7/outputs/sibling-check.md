# Step 4 -- Duplicate, Sibling, and Overlap Check: TC-8006

## Step 4 JQL Search

Query (simulated):
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

### Search Results

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|------------------|---------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

## Sibling Classification

- **TC-8006** stream suffix: `[rhtpa-2.1]` (stream 2.1.x)
- **TC-8001** stream suffix: `[rhtpa-2.2]` (stream 2.2.x)

TC-8001 has a **different** stream suffix from TC-8006. Classification: **different-stream sibling** (companion tracker, not a duplicate).

### Step 4.1 -- Same-Stream Duplicate Check

No same-stream siblings found. TC-8001 is on stream 2.2.x while TC-8006 is on stream 2.1.x. No duplicate action required.

### Step 4.2 -- Cross-Stream Coordination

TC-8001 is a different-stream companion tracker. Per Step 4.2 procedure:

**1. Check for existing link before creating one.**

Read the current issue's (TC-8006) `issuelinks` array from the `jira.get_issue` response fetched in Step 1. The existing links are:

| Link ID | Type | Direction | Linked Issue |
|---------|------|-----------|--------------|
| 1990401 | Related | outward (TC-8006 -> TC-8001) | TC-8001 |

Checking if any existing link satisfies ALL of:
- `type.name` is `"Related"` -- YES (type is "Related")
- `outwardIssue.key` matches the sibling key TC-8001 -- YES

**Result: A matching Related link to TC-8001 already exists.**

> Related link to TC-8001 already exists -- skipping link creation.

Link creation is skipped (idempotent behavior).

**2. Verify no Affects Versions overlap.**

- TC-8006 Affects Versions: RHTPA 2.1.0 (stream 2.1.x)
- TC-8001 Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1 (stream 2.2.x)

No version overlap detected. Each issue carries only versions from its own stream.

**3. Sibling landscape presentation:**

```
CVE-2026-31812 companion issues:

| Issue       | Stream | Status      | Affects Versions               |
|-------------|--------|-------------|---------------------------------|
| TC-8001     | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1       |
| TC-8006 <-  | 2.1.x  | New         | RHTPA 2.1.0                     |
```

The arrow `<-` indicates the current issue being triaged.

### Step 4.3 -- Cross-CVE Overlap Detection

The Upstream Affected Component custom field, PS Component custom field, and Stream custom field are NOT configured in the project's Security Configuration (claude-md-security-config.md). Per the skill instructions: "If any of these fields are not configured, skip this step entirely."

**Skipped.**

### Step 4.4 -- Preemptive Task Reconciliation

Search for preemptive tasks matching CVE-2026-31812 for stream rhtpa-2.1 (simulated):

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```

No matching preemptive tasks found for this CVE and stream. Proceeding to Step 5.
