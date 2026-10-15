# Step 4 -- Duplicate, Sibling, and Overlap Check: TC-8003

## JQL Search Results

A JQL search for sibling Vulnerability issues with the same CVE label returned:

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8003
```

**Results: 1 sibling found**

| Issue | Summary | Status | Stream Suffix | Affects Versions |
|-------|---------|--------|---------------|------------------|
| TC-7999 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | [rhtpa-2.2] | RHTPA 2.2.0, RHTPA 2.2.1 |

## Step 4.1 -- Same-Stream Duplicate Analysis

### Stream comparison

- **TC-8003** (current issue): stream suffix `[rhtpa-2.2]` --> stream **2.2.x**
- **TC-7999** (sibling issue): stream suffix `[rhtpa-2.2]` --> stream **2.2.x**

Both issues have the **same** stream suffix `[rhtpa-2.2]`, making TC-7999 a **same-stream sibling**.

### Duplicate classification

Per Step 4.1 of the triage-security skill: "If a same-stream sibling exists and is open or in progress: Recommendation: Close the current issue as Duplicate."

- TC-7999 status: **In Progress** (open and actively being worked)
- TC-8003 status: **New** (untriaged)
- Same CVE: CVE-2026-31812
- Same stream: 2.2.x
- Same component: pscomponent:org/rhtpa-server

**Conclusion: TC-8003 is a duplicate of TC-7999.**

TC-7999 is already In Progress with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1], which covers the same affected versions within the 2.2.x stream. The version impact analysis shows RHTPA 2.2.2 (retag of 2.2.1) is also affected but that can be addressed on TC-7999 if its Affects Versions need correction.

### Affects Versions note

TC-8003 currently claims only `RHTPA 2.2.0`, while the version impact analysis shows `RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2` are affected. However, since TC-8003 is a duplicate, the Affects Versions correction is not needed on TC-8003 -- TC-7999 already carries RHTPA 2.2.0 and RHTPA 2.2.1, and should be separately verified for RHTPA 2.2.2 coverage.

## Steps 4.2, 4.3, 4.4

- **Step 4.2 (Cross-stream coordination)**: Not applicable -- TC-7999 is a same-stream sibling, not a different-stream companion.
- **Step 4.3 (Cross-CVE overlap detection)**: Skipped -- the Upstream Affected Component custom field, PS Component custom field, and Stream custom field are not configured in the mock Security Configuration.
- **Step 4.4 (Preemptive task reconciliation)**: Not applicable -- the issue will be closed as duplicate, so no remediation tasks will be created.
