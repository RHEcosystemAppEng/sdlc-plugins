# Step 4 -- Duplicate, Sibling, and Overlap Check for TC-8006

## JQL Search for Siblings

Simulated JQL query:
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

Results: **1 sibling found**

| Key | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-----|---------|--------|--------|------------------|---------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

## Step 4.1 -- Same-Stream Duplicate Check

- TC-8006 stream suffix: `[rhtpa-2.1]` (stream 2.1.x)
- TC-8001 stream suffix: `[rhtpa-2.2]` (stream 2.2.x)
- Classification: **Different-stream sibling** (companion tracker)

No same-stream duplicates found. Proceeding to Step 4.2.

## Step 4.2 -- Cross-Stream Coordination

TC-8001 is a **companion tracker** for the same CVE in a different stream. PSIRT
creates one issue per stream intentionally -- this is not a duplicate.

### Link Idempotency Check

Per Step 4.2 procedure: before creating a link, check the current issue's
`issuelinks` array (already fetched in Step 1) for an existing link where:
- `type.name` is `"Related"`, AND
- `inwardIssue.key` or `outwardIssue.key` matches the sibling key (TC-8001)

**Existing links on TC-8006:**
- Link ID 1990401: type = "Related", direction = outward, outwardIssue.key = **TC-8001**

**Result: A matching Related link to TC-8001 already exists.**

Action: **Skip link creation.** Log:
> "Related link to TC-8001 already exists -- skipping"

No `jira.create_link` call is made. The pre-existing link satisfies the
cross-stream coordination requirement.

### Affects Versions Overlap Check

Verify no Affects Versions overlap between the two issues:

| Issue | Stream | Affects Versions |
|-------|--------|------------------|
| TC-8006 | 2.1.x | RHTPA 2.1.0 |
| TC-8001 | 2.2.x | RHTPA 2.2.0, RHTPA 2.2.1 |

**No overlap detected.** Each issue carries only versions from its own stream.

### Sibling Landscape

CVE-2026-31812 companion issues:

| Issue | Stream | Status | Affects Versions |
|-------|--------|--------|------------------|
| TC-8001 | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |
| TC-8006 (current) | 2.1.x | New | RHTPA 2.1.0 |
