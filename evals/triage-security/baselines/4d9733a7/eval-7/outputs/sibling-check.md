# Step 4 -- Duplicate, Sibling, and Overlap Check

## Sibling Search

**JQL query** (proposed, not executed):
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

**Mock result** (from eval fixture): 1 sibling found.

| Sibling | Summary | Status | Stream Suffix | Affects Versions |
|---------|---------|--------|---------------|------------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | [rhtpa-2.2] | RHTPA 2.2.0, RHTPA 2.2.1 |

## Step 4.1 -- Same-Stream Duplicate Check

Current issue stream suffix: `[rhtpa-2.1]`
Sibling TC-8001 stream suffix: `[rhtpa-2.2]`

**Classification**: TC-8001 is a **different-stream companion** (stream [rhtpa-2.2] vs current issue's [rhtpa-2.1]). This is NOT a same-stream duplicate. PSIRT creates one issue per stream intentionally.

## Step 4.2 -- Cross-Stream Coordination

TC-8001 is a different-stream sibling (companion tracker). Per Step 4.2, before creating a "Related" link, check the current issue's existing `issuelinks` array.

### Pre-existing Link Check

Checking TC-8006's existing `issuelinks` (from the `jira.get_issue` response fetched in Step 1):

| Existing Link Type | Direction | Target |
|--------------------|-----------|--------|
| Related | outward | TC-8001 |

**Result**: A pre-existing "Related" link to TC-8001 already exists on TC-8006.

> **Related link to TC-8001 already exists -- skipping link creation.**

The skill does NOT call `jira.create_link` because the link already satisfies all conditions:
- `type.name` is "Related"
- `outwardIssue.key` matches the sibling key (TC-8001)

The idempotent check prevents duplicate link creation.

## Sibling Landscape Table

Despite the link already existing, the sibling landscape is still presented to the engineer for visibility:

```
CVE-2026-31812 companion issues:

| Issue      | Stream | Status      | Affects Versions              |
|------------|--------|-------------|-------------------------------|
| TC-8001    | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1     |
| TC-8006 <- | 2.1.x  | New         | RHTPA 2.1.0                   |
```

The arrow `<-` indicates the current issue being triaged.

No Affects Versions overlap detected between TC-8006 and TC-8001 (different streams -- 2.1.x vs 2.2.x).
