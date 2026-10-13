# Duplicate Check — TC-8003

## Step 4 — Duplicate, Sibling, and Overlap Check

### JQL Search

A JQL search for sibling Vulnerability issues with the same CVE label was performed:

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8003
```

### Search Results

One sibling issue found:

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|-----------------|---------------|
| TC-7999 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

### Sibling Classification

- **TC-8003** stream suffix: `[rhtpa-2.2]` --> stream **2.2.x**
- **TC-7999** stream suffix: `[rhtpa-2.2]` --> stream **2.2.x**

Classification: **Same-stream sibling** (both issues are scoped to the 2.2.x stream)

### Step 4.1 — Same-Stream Duplicate Analysis

TC-7999 is a same-stream sibling that is currently **In Progress** (open and actively being worked on).

Per the skill's Step 4.1 procedure:
- A same-stream sibling exists and is open/in progress.
- TC-7999 already has broader Affects Versions coverage: `RHTPA 2.2.0, RHTPA 2.2.1`
- TC-8003 only has: `RHTPA 2.2.0`
- TC-7999's Affects Versions already subsume TC-8003's Affects Versions.

**Recommendation**: Close TC-8003 as **Duplicate** of TC-7999.

### Proposed Actions (pending engineer confirmation)

1. **Add comment** to TC-8003:
   > "Duplicate of TC-7999 -- same CVE (CVE-2026-31812) tracked for the same stream (2.2.x). TC-7999 is already In Progress with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1], which subsumes this issue's Affects Versions [RHTPA 2.2.0]. Version impact analysis confirms overlap."

2. **Transition** TC-8003 to Closed with resolution **"Duplicate"**.

3. **Assign** TC-8003 to current user.

### Steps 4.2, 4.3, 4.4 — Not Applicable

- **Step 4.2 (Cross-stream coordination)**: Not applicable. TC-7999 is a same-stream sibling, not a different-stream companion.
- **Step 4.3 (Cross-CVE overlap detection)**: Skipped. The Upstream Affected Component custom field is not configured in Security Configuration.
- **Step 4.4 (Preemptive task reconciliation)**: Not applicable. TC-8003 is being closed as a duplicate, so no remediation tasks will be created for this issue. Preemptive task reconciliation is only relevant when proceeding to Step 8.
