# Step 4 -- Duplicate, Sibling, and Overlap Check: TC-8003

## 4.0 -- JQL Search for Sibling Issues

Search for sibling Vulnerability issues with the same CVE label, excluding the current issue:

```
jira.search_jql(
  "project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8003"
)
```

### Results

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|------------------|---------------|
| TC-7999 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

## 4.1 -- Same-Stream Duplicate Analysis

### Stream comparison

- **TC-8003** stream suffix: `[rhtpa-2.2]` --> stream **2.2.x**
- **TC-7999** stream suffix: `[rhtpa-2.2]` --> stream **2.2.x**

Both issues have the same stream suffix `[rhtpa-2.2]`, mapping to the **2.2.x** version stream.

### Classification: **Same-stream sibling**

TC-7999 is a **same-stream sibling** of TC-8003. Both track CVE-2026-31812 for the identical stream (2.2.x). TC-7999 is already **In Progress** with Affects Versions covering RHTPA 2.2.0 and RHTPA 2.2.1.

### Duplicate determination

Per Step 4.1 of the triage procedure: "If a same-stream sibling exists and is open or in progress, recommend closing the current issue as Duplicate."

TC-7999 is in status **In Progress** (open and actively being worked). TC-8003 is a duplicate -- it tracks the same CVE (CVE-2026-31812) for the same stream (2.2.x) as TC-7999.

**Recommendation**: Close TC-8003 as **Duplicate** of TC-7999.

## Short-Circuit

Duplicate detection short-circuits the triage flow. Steps 4.2, 4.3, 4.4, 5, 6, and 7 are skipped. No remediation tasks are created.
