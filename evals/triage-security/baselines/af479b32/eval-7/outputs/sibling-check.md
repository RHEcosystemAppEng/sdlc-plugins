# Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check: TC-8006

## Step 4 -- Sibling Search

### JQL Query (simulated)

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

### Results

One sibling issue found:

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|------------------|---------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

### Sibling Classification

- **TC-8001** -- stream suffix `[rhtpa-2.2]` maps to stream **2.2.x**
- **TC-8006** (current issue) -- stream suffix `[rhtpa-2.1]` maps to stream **2.1.x**

These are **different-stream siblings** (companion trackers). TC-8001 is NOT a same-stream duplicate.

## Step 4.1 -- Same-Stream Duplicate Check

No same-stream siblings found. TC-8001 belongs to stream 2.2.x while TC-8006 belongs to stream 2.1.x. No duplicate closure required.

## Step 4.2 -- Cross-Stream Coordination

TC-8001 is a different-stream sibling (companion tracker for the 2.2.x stream). Per Step 4.2 of jira-triage-operations.md, the skill must check for an existing link before creating one.

### Link Idempotency Check

The current issue's `issuelinks` array (fetched in Step 1) contains the following link:

- Link ID: 1990401
- Type name: **Related**
- Direction: outward
- Outward issue key: **TC-8001**

**Check criteria** (all must be satisfied to skip link creation):
1. `type.name` is `"Related"` -- YES (link type is "Related")
2. `inwardIssue.key` or `outwardIssue.key` matches the sibling key TC-8001 -- YES (`outwardIssue.key` = TC-8001)

All criteria are satisfied. A matching "Related" link to TC-8001 already exists on TC-8006.

### Result: Link creation SKIPPED

> "Related link to TC-8001 already exists -- skipping"

No Jira mutation is performed. The existing link (ID 1990401) is sufficient. This is the idempotent behavior specified in Step 4.2: "If a matching link exists, skip link creation and log."

### Affects Versions Overlap Check

- **TC-8006** (2.1.x stream): Affects Versions = [RHTPA 2.1.0]
- **TC-8001** (2.2.x stream): Affects Versions = [RHTPA 2.2.0, RHTPA 2.2.1]

No version overlap detected. Each issue carries only versions from its own stream, as expected.

### Sibling Landscape

```
CVE-2026-31812 companion issues:

| Issue      | Stream | Status      | Affects Versions              |
|------------|--------|-------------|-------------------------------|
| TC-8001    | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1     |
| TC-8006 <- | 2.1.x  | New         | RHTPA 2.1.0                   |
```

Note: TC-8006 (current issue) is marked with `<-`. TC-8001 is already "In Progress", meaning triage or remediation work has begun on the 2.2.x stream.

## Step 4.3 -- Cross-CVE Overlap Detection

**SKIPPED.** The Upstream Affected Component custom field, PS Component custom field, and Stream custom field are not configured in the project's Security Configuration. Per the skill specification, Step 4.3 is skipped entirely when these fields are not configured.

## Step 4.4 -- Preemptive Task Reconciliation

### JQL Query (simulated)

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```

### Result

No preemptive remediation tasks found matching CVE-2026-31812 for the 2.1.x stream. Proceeding to Step 5.
