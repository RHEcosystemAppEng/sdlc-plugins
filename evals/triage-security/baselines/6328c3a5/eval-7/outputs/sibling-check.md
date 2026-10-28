# Step 4 -- Duplicate, Sibling, and Overlap Check for TC-8006

## Step 4.0 -- JQL Sibling Search

A JQL search for sibling Vulnerability issues with the same CVE label was
performed (simulated):

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

### Search Results

One sibling found:

| Issue | Summary | Status | Stream Suffix | Affects Versions |
|-------|---------|--------|---------------|------------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | [rhtpa-2.2] | RHTPA 2.2.0, RHTPA 2.2.1 |

## Step 4.1 -- Same-Stream Duplicate Check

TC-8001 has stream suffix `[rhtpa-2.2]`, while TC-8006 has stream suffix
`[rhtpa-2.1]`. These are **different streams** (2.2.x vs 2.1.x).

**Result**: TC-8001 is NOT a same-stream duplicate. It is a cross-stream
companion tracker. Proceeding to Step 4.2.

## Step 4.2 -- Cross-Stream Coordination

TC-8001 is a **different-stream sibling** (companion tracker). Per the skill
procedure, before creating a Related link, the current issue's `issuelinks`
array must be checked for an existing link.

### Existing Link Check

Reading TC-8006's `issuelinks` from the issue data fetched in Step 1:

- Link ID: 1990401
- Link type name: "Related"
- Direction: outward (TC-8006 -> TC-8001)
- Target issue key: TC-8001

**Check criteria** (all three must be satisfied):
1. `type.name` is "Related" -- YES
2. `outwardIssue.key` matches the sibling key TC-8001 -- YES
3. Link is present and active -- YES (link ID 1990401)

**All criteria satisfied.** A matching Related link to TC-8001 already exists
on TC-8006.

### Decision: Skip Link Creation

Per Step 4.2 of jira-triage-operations.md:

> "If a matching link exists, skip link creation and log:
> 'Related link to [sibling-key] already exists -- skipping'"

**Action taken**: Related link to TC-8001 already exists -- skipping.

No `jira.create_link()` call is made. The pre-existing link (ID 1990401)
provides the required cross-stream coordination traceability.

### Affects Versions Overlap Verification

- TC-8006 Affects Versions: RHTPA 2.1.0 (stream 2.1.x)
- TC-8001 Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1 (stream 2.2.x)

**No overlap detected.** Each issue carries only versions from its own stream.
The version scoping is correct.

### Sibling Landscape

```
CVE-2026-31812 companion issues:

| Issue      | Stream | Status      | Affects Versions              |
|------------|--------|-------------|-------------------------------|
| TC-8001    | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1     |
| TC-8006 <- | 2.1.x  | New         | RHTPA 2.1.0                   |
```

The arrow (`<-`) indicates the current issue being triaged.

## Step 4.3 -- Cross-CVE Overlap Detection

The Upstream Affected Component custom field is NOT configured in the project's
Security Configuration. Per the skill procedure:

> "If any of these fields are not configured, skip this step entirely."

**Result**: Step 4.3 skipped -- no Upstream Affected Component custom field
configured.

## Step 4.4 -- Preemptive Task Reconciliation

A search for preemptive tasks matching CVE-2026-31812 and the 2.1.x stream
would be performed. Based on the available information, no preemptive
remediation tasks exist for this CVE and stream combination.

**Result**: No matching preemptive task found. Proceeding to Step 5.
