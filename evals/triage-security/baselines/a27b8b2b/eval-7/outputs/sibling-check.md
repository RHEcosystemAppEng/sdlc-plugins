# Step 4 -- Duplicate, Sibling, and Overlap Check

## 4.0 -- Sibling Search

JQL query executed (proposed -- not actually called per eval rules):

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

**Results**: 1 sibling issue found.

| Issue | Summary | Stream Suffix | Status | Affects Versions |
|-------|---------|---------------|--------|-----------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | [rhtpa-2.2] | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |

## 4.1 -- Same-Stream Duplicate Check

- Current issue TC-8006 stream: **[rhtpa-2.1]** (2.1.x)
- Sibling TC-8001 stream: **[rhtpa-2.2]** (2.2.x)
- Classification: **Different-stream companion** -- NOT a same-stream duplicate.

TC-8001 tracks the same CVE (CVE-2026-31812) but for a different product version stream. PSIRT creates one Vulnerability issue per stream intentionally. These are companion trackers, not duplicates.

No duplicate closure is warranted. Proceed to Step 4.2 (Cross-stream coordination).

## 4.2 -- Cross-Stream Coordination

### Pre-existing Link Check (Idempotency)

Before creating a Related link to sibling TC-8001, check TC-8006's existing `issuelinks` array (already fetched in Step 1).

**Existing links on TC-8006:**

| Link Type | Direction | Linked Issue |
|-----------|-----------|--------------|
| Related | outward | TC-8001 |

**Idempotency check result:**
- Link type: "Related" -- MATCHES
- Linked issue: TC-8001 -- MATCHES

> Related link to TC-8001 already exists -- skipping

The pre-existing Related link to TC-8001 satisfies the cross-stream coordination requirement. `jira.create_link` is NOT called -- creating a duplicate link would be redundant.

### Affects Versions Overlap Check

- TC-8006 Affects Versions: RHTPA 2.1.0 (stream 2.1.x)
- TC-8001 Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1 (stream 2.2.x)

No version overlap detected -- each issue carries versions from its own stream only. This is the expected state.

### Sibling Landscape

Despite the link already existing (and link creation being skipped), the sibling landscape table is presented to the engineer for situational awareness:

```
CVE-2026-31812 companion issues:

| Issue      | Stream | Status      | Affects Versions              |
|------------|--------|-------------|-------------------------------|
| TC-8001    | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1     |
| TC-8006 <- | 2.1.x  | New         | RHTPA 2.1.0                   |
```

The arrow (`<-`) indicates the current issue being triaged.

**Note**: The idempotent link check only affects link creation -- the sibling summary is always presented regardless of whether a link was created or already existed.

## 4.3 -- Cross-CVE Overlap Detection

The Upstream Affected Component custom field is not configured in the Security Configuration for this project (no `customfield_10632` or equivalent listed). Step 4.3 is skipped entirely.

## 4.4 -- Preemptive Task Reconciliation

No preemptive tasks were found for CVE-2026-31812 in stream rhtpa-2.1. Proceeding to Step 5.
