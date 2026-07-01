# Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check

## 4.0 -- Sibling Search

Searched for sibling Vulnerability issues with the same CVE label using JQL:

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

**Results**: 1 sibling found.

| Sibling Key | Summary | Status | Stream Suffix | Affects Versions |
|-------------|---------|--------|---------------|------------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | [rhtpa-2.2] | RHTPA 2.2.0, RHTPA 2.2.1 |

## 4.1 -- Same-Stream Duplicate Check

Comparing stream suffixes:

- **Current issue (TC-8006)**: stream suffix `[rhtpa-2.1]` -- stream **2.1.x**
- **Sibling (TC-8001)**: stream suffix `[rhtpa-2.2]` -- stream **2.2.x**

The streams are **different** (`2.1.x` vs `2.2.x`). TC-8001 is classified as a **different-stream companion**, NOT a same-stream duplicate.

**Result**: No same-stream duplicates detected. TC-8001 is a cross-stream companion tracker -- PSIRT creates one issue per stream intentionally.

## 4.2 -- Cross-Stream Coordination

TC-8001 is a different-stream sibling (companion tracker). Per Step 4.2 procedure:

### Pre-existing Link Check

Before attempting to create a "Related" link to TC-8001, checking the current issue's existing `issuelinks` array (fetched in Step 1):

**Existing links on TC-8006:**

| Link ID | Type | Direction | Linked Issue |
|---------|------|-----------|--------------|
| 1990401 | Related | outward (TC-8006 -> TC-8001) | TC-8001 |

Checking link criteria:
- `type.name` is `"Related"` -- **YES**
- `outwardIssue.key` matches the sibling key `TC-8001` -- **YES**

**All criteria satisfied.** A matching "Related" link to TC-8001 already exists on this issue.

> Related link to TC-8001 already exists -- skipping link creation.

No call to `jira.create_link` is made. The existing link (ID: 1990401) already establishes the cross-stream relationship.

### Affects Versions Overlap Check

Verifying no Affects Versions overlap between the two companion issues:

| Issue | Stream | Affects Versions |
|-------|--------|------------------|
| TC-8006 | 2.1.x | RHTPA 2.1.0 |
| TC-8001 | 2.2.x | RHTPA 2.2.0, RHTPA 2.2.1 |

No overlap detected -- each issue carries versions only from its own stream.

### Sibling Landscape

Despite the link already existing, the sibling landscape is presented to the engineer for situational awareness:

```
CVE-2026-31812 companion issues:

| Issue      | Stream | Status      | Affects Versions              | Link Status |
|------------|--------|-------------|-------------------------------|-------------|
| TC-8001    | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1     | Related (pre-existing) |
| TC-8006 <- | 2.1.x  | New         | RHTPA 2.1.0                   | (current issue) |
```

The arrow (`<-`) indicates the current issue being triaged.

**Note**: The idempotent link check only affects link creation -- it does not suppress the sibling landscape summary. The engineer needs visibility into the full companion issue landscape regardless of whether links were newly created or already existed.

## 4.3 -- Cross-CVE Overlap Detection

The Upstream Affected Component custom field is not configured in the Security Configuration for this project. Skipping Step 4.3.

## 4.4 -- Preemptive Task Reconciliation

No preemptive task search performed -- proceeding to Step 5.

## Summary

| Check | Result |
|-------|--------|
| Same-stream duplicate | No -- TC-8001 is a different stream (2.2.x vs 2.1.x) |
| Cross-stream companion | TC-8001 (2.2.x, In Progress) |
| Link creation | **Skipped** -- Related link to TC-8001 already exists (link ID: 1990401) |
| Affects Versions overlap | None detected |
| Cross-CVE overlap | Skipped (Upstream Affected Component field not configured) |
| Preemptive reconciliation | No preemptive tasks found |
