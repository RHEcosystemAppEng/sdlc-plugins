# Step 4 -- Duplicate, Sibling, and Overlap Check for TC-8006

## Step 4 JQL Search

Simulated JQL:
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

Results: **1 sibling found**

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|------------------|---------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

## Sibling Classification

- **TC-8006** stream suffix: `[rhtpa-2.1]` (stream 2.1.x)
- **TC-8001** stream suffix: `[rhtpa-2.2]` (stream 2.2.x)
- Classification: **Different-stream sibling** (companion tracker, NOT a duplicate)

TC-8001 is a cross-stream companion issue -- PSIRT created one Vulnerability issue per stream intentionally. This is standard PSIRT behavior and does not indicate duplication.

## Step 4.1 -- Same-Stream Duplicate Check

No same-stream siblings found. TC-8001 has a different stream suffix (`[rhtpa-2.2]` vs `[rhtpa-2.1]`), so it is not a same-stream duplicate.

Result: **No duplicates detected. Proceed.**

## Step 4.2 -- Cross-Stream Coordination

### Link Idempotency Check

Per Step 4.2, before creating a Related link to the sibling TC-8001, the skill checks the current issue's existing `issuelinks` array (already fetched in Step 1).

**Existing links on TC-8006:**

| Link ID | Type | Direction | Target |
|---------|------|-----------|--------|
| 1990401 | Related | outward (TC-8006 -> TC-8001) | TC-8001 |

**Check criteria (all must match):**
1. `type.name` is `"Related"` -- YES (link type is Related)
2. `outwardIssue.key` matches the sibling key TC-8001 -- YES

**Result: A matching Related link to TC-8001 already exists.**

**Action: SKIP link creation.**

Log message:
> "Related link to TC-8001 already exists -- skipping"

No `jira.create_link` call is proposed. The pre-existing link satisfies the cross-stream coordination requirement without modification.

### Affects Versions Overlap Check

- TC-8006 Affects Versions: `[RHTPA 2.1.0]`
- TC-8001 Affects Versions: `[RHTPA 2.2.0, RHTPA 2.2.1]`

No version overlap detected. Each issue carries only versions from its own stream, which is correct.

### Sibling Landscape

```
CVE-2026-31812 companion issues:

| Issue       | Stream | Status      | Affects Versions               |
|-------------|--------|-------------|--------------------------------|
| TC-8001     | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1      |
| TC-8006 <-  | 2.1.x  | New         | RHTPA 2.1.0                    |
```

The arrow (`<-`) indicates the current issue being triaged.

## Step 4.3 -- Cross-CVE Overlap Detection

The Upstream Affected Component custom field, PS Component custom field, and Stream custom field are **not configured** in the project's Security Configuration. Per the skill procedure, Step 4.3 is **skipped entirely** when these fields are not configured.

Result: **Skipped -- required custom fields not configured.**

## Step 4.4 -- Preemptive Task Reconciliation

Simulated JQL for preemptive tasks:
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```

Assumed result: **No matching preemptive tasks found** for CVE-2026-31812 in the 2.1.x stream.

Result: **No preemptive tasks to reconcile. Proceed to Step 5.**

## Summary of Step 4 Proposed Actions

| Action | Target | Status |
|--------|--------|--------|
| Create Related link TC-8006 -> TC-8001 | TC-8001 | **SKIPPED** (link already exists, link ID 1990401) |
| Close as duplicate | TC-8006 | **NOT APPLICABLE** (TC-8001 is a different-stream companion, not a same-stream duplicate) |
| Cross-CVE overlap check | -- | **SKIPPED** (Upstream Affected Component field not configured) |
| Preemptive task reconciliation | -- | **No match** (no preemptive tasks found) |
