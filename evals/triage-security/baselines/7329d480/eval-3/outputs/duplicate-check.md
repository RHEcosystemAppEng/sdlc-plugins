# Duplicate Check (Step 4) -- TC-8003

## JQL Sibling Search

Query: `project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8003`

### Results

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|------------------|---------------|
| TC-7999 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

## Stream Classification

- **TC-8003** stream suffix: `[rhtpa-2.2]` --> stream 2.2.x
- **TC-7999** stream suffix: `[rhtpa-2.2]` --> stream 2.2.x

Both issues have the **same stream suffix** `[rhtpa-2.2]`. TC-7999 is therefore a **same-stream sibling**.

## Step 4.1 -- Same-Stream Duplicate Analysis

TC-7999 is a same-stream sibling with the same CVE (CVE-2026-31812) targeting the same stream (2.2.x).

- TC-7999 status: **In Progress** (open and actively being worked on)
- TC-7999 Affects Versions: **RHTPA 2.2.0, RHTPA 2.2.1** (already has the correct scope)
- TC-8003 status: **New** (not yet triaged)

Per the triage-security skill Step 4.1: when a same-stream sibling exists and is open or in progress, the recommendation is to **close the current issue (TC-8003) as Duplicate**.

### Recommendation

**Close TC-8003 as Duplicate of TC-7999.**

TC-7999 is already In Progress for the same CVE (CVE-2026-31812) in the same stream (2.2.x), with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1] that already cover the correct version scope. There is no need for a second tracker for the same CVE in the same stream.

### Proposed Jira Actions (pending engineer confirmation)

1. Add comment to TC-8003: "Duplicate of TC-7999 -- same CVE (CVE-2026-31812) tracked for the same stream [rhtpa-2.2]. Version impact analysis confirms overlap. TC-7999 is already In Progress with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1]."
2. Transition TC-8003 to Closed with resolution "Duplicate".
3. Assign TC-8003 to current user.

## Steps 4.2, 4.3, 4.4

- **Step 4.2 (Cross-stream coordination)**: Not applicable -- TC-7999 is a same-stream sibling, not a different-stream companion.
- **Step 4.3 (Cross-CVE overlap)**: Skipped -- Upstream Affected Component custom field is not configured in Security Configuration.
- **Step 4.4 (Preemptive task reconciliation)**: Not applicable -- the issue is being closed as duplicate, so no reconciliation is needed.
