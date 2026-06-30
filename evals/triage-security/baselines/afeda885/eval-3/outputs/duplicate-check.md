# Step 4 -- Duplicate, Sibling, and Overlap Check: TC-8003

## 4.0 -- JQL Query for Sibling Issues

The following JQL query was used to search for sibling Vulnerability issues with the same CVE label, excluding the current issue:

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8003
```

### Query Results

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|------------------|---------------|
| TC-7999 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

**Siblings found: 1**

## 4.1 -- Same-Stream Duplicate Analysis

### Stream comparison

| Issue | Stream Suffix | Mapped Stream |
|-------|---------------|---------------|
| TC-8003 (current) | [rhtpa-2.2] | 2.2.x |
| TC-7999 (sibling) | [rhtpa-2.2] | 2.2.x |

**Classification: Same-stream sibling** -- both TC-8003 and TC-7999 carry the stream suffix `[rhtpa-2.2]`, mapping to the same 2.2.x version stream.

### Duplicate determination

TC-7999 is a **same-stream sibling** that:
- Tracks the **same CVE**: CVE-2026-31812
- Targets the **same stream**: 2.2.x (both have suffix `[rhtpa-2.2]`)
- Has a **more advanced status**: In Progress (vs. TC-8003's New status)
- Has **more complete Affects Versions**: RHTPA 2.2.0, RHTPA 2.2.1 (TC-8003 only has RHTPA 2.2.0)

Per Step 4.1 of the triage procedure, when a same-stream sibling exists and is open or in progress, the recommendation is to **close the current issue as Duplicate**.

### Recommendation

**Close TC-8003 as Duplicate of TC-7999.**

TC-7999 is already In Progress, covering the same CVE (CVE-2026-31812) for the same stream (2.2.x) with a more complete Affects Versions set (RHTPA 2.2.0, RHTPA 2.2.1). Maintaining two issues tracking the identical vulnerability in the identical stream would create redundant tracking and risk conflicting remediation efforts.

### Proposed Jira actions (pending engineer confirmation)

1. **Add comment to TC-8003:**

   > Duplicate of TC-7999 -- same CVE (CVE-2026-31812) tracked for the same stream [rhtpa-2.2]. TC-7999 is already In Progress with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1] and covers this issue's scope entirely. Closing as duplicate. Version impact analysis confirms overlap: both issues target the 2.2.x stream where quinn-proto ships at versions below the 0.11.14 fix threshold.

2. **Transition TC-8003** to Closed with resolution **Duplicate**.

3. **Assign TC-8003** to current user.

## 4.2 -- Cross-Stream Coordination

Not applicable. No different-stream siblings were found in the JQL results. The only sibling (TC-7999) is a same-stream match, handled in 4.1 above.

## 4.3 -- Cross-CVE Overlap Detection

Skipped. Duplicate detection in Step 4.1 short-circuits the triage -- there is no need to check for cross-CVE overlap when the issue will be closed as a duplicate.

## 4.4 -- Preemptive Task Reconciliation

Skipped. Duplicate detection in Step 4.1 short-circuits the triage -- there is no need to search for preemptive tasks when the issue will be closed as a duplicate.
