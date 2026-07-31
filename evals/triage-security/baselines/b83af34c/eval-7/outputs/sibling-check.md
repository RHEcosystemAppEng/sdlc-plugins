# Step 4 -- Duplicate, Sibling, and Overlap Check for TC-8006

## Step 4 -- JQL Sibling Search

Simulated JQL query:
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

Results: **1 sibling found**

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|------------------|---------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

## Sibling Classification

- **Current issue TC-8006**: stream suffix `[rhtpa-2.1]` -> stream **2.1.x**
- **Sibling TC-8001**: stream suffix `[rhtpa-2.2]` -> stream **2.2.x**
- **Classification**: **Different-stream companion** (not a same-stream duplicate)

TC-8001 is scoped to stream 2.2.x while TC-8006 is scoped to stream 2.1.x. These are companion trackers -- PSIRT creates one Vulnerability issue per stream intentionally. This is NOT a duplicate.

## Step 4.1 -- Same-Stream Duplicate Check

No same-stream siblings found. TC-8001 belongs to a different stream (2.2.x vs 2.1.x). No duplicate closure recommended.

## Step 4.2 -- Cross-Stream Coordination

### Idempotent Link Check (per SKILL.md section 1.58 / Step 4.2)

Before attempting to create a 'Related' link to TC-8001, Step 4.2 requires checking the current issue's existing `issuelinks` array (already fetched in Step 1 via `jira.get_issue`).

**Check performed**: Inspecting TC-8006's issuelinks for any link where:
- `type.name` is "Related"
- `inwardIssue.key` or `outwardIssue.key` matches "TC-8001"

**Result**: Found existing link:
- Link ID: 1990401
- Type: Related
- Direction: outward (TC-8006 -> TC-8001)
- `outwardIssue.key` = TC-8001

**Decision**: A matching Related link to TC-8001 already exists.

> Related link to TC-8001 already exists -- skipping

`jira.create_link` was NOT called. The link creation was skipped because the pre-existing link satisfies the idempotent check.

### Affects Versions Overlap Check

- TC-8006 Affects Versions: RHTPA 2.1.0 (stream 2.1.x)
- TC-8001 Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1 (stream 2.2.x)

No overlap detected -- each issue carries only versions from its own stream.

### Sibling Landscape Table

Despite the link already existing (and link creation being skipped), the sibling landscape is still presented to the engineer for situational awareness:

```
CVE-2026-31812 companion issues:

| Issue      | Stream | Status      | Affects Versions              |
|------------|--------|-------------|-------------------------------|
| TC-8001    | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1     |
| TC-8006 <- | 2.1.x  | New         | RHTPA 2.1.0                   |
```

The idempotent check only affects link creation -- it does not suppress the sibling summary. The engineer needs the full cross-stream picture regardless of whether links needed to be created or already existed.
