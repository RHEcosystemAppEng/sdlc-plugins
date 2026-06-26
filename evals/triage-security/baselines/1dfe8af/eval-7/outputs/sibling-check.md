# Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check

## Step 4 JQL Search

Query:
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

Results: **1 sibling found**

| Issue Key | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-----------|---------|--------|--------|------------------|---------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

## Sibling Classification

- **TC-8001**: Stream suffix `[rhtpa-2.2]` vs current issue TC-8006 stream suffix `[rhtpa-2.1]`
- Classification: **Different-stream companion** (NOT a same-stream duplicate)
- Rationale: TC-8001 tracks the same CVE (CVE-2026-31812) for the 2.2.x stream, while TC-8006 tracks it for the 2.1.x stream. PSIRT creates one Vulnerability issue per stream intentionally -- these are companion trackers, not duplicates.

## Step 4.1 -- Same-Stream Duplicate Check

No same-stream siblings found. TC-8001 is a different-stream companion. No duplicate closure recommended.

## Step 4.2 -- Cross-Stream Coordination

### Link Check for TC-8001

Checking existing `issuelinks` on TC-8006 (from Step 1 data extraction) for a pre-existing Related link to TC-8001:

- Existing link found: **Link ID 1990401**, type `Related`, direction `outward` (TC-8006 -> TC-8001)
- The link `type.name` is `"Related"` and `outwardIssue.key` matches `TC-8001`
- **All conditions satisfied** -- a matching Related link already exists

**Result: Related link to TC-8001 already exists -- skipping link creation.**

> Related link to TC-8001 already exists -- skipping

No `jira.create_link` call is made. The existing link (ID 1990401) already establishes the cross-stream relationship between TC-8006 and TC-8001.

### Affects Versions Overlap Check

- TC-8006 Affects Versions: RHTPA 2.1.0 (stream 2.1.x)
- TC-8001 Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1 (stream 2.2.x)
- **No overlap detected** -- each issue carries only versions from its own stream.

### Sibling Landscape Table

CVE-2026-31812 companion issues:

| Issue | Stream | Status | Affects Versions |
|-------|--------|--------|------------------|
| TC-8001 | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |
| TC-8006 (current) | 2.1.x | New | RHTPA 2.1.0 |

## Step 4.3 -- Cross-CVE Overlap Detection

Skipped. The Upstream Affected Component custom field, PS Component custom field, and Stream custom field are not configured in Security Configuration. Cross-CVE overlap detection requires all three fields.

## Step 4.4 -- Preemptive Task Reconciliation

No preemptive tasks found for CVE-2026-31812 in the 2.1.x stream. Proceeding to Step 5.
