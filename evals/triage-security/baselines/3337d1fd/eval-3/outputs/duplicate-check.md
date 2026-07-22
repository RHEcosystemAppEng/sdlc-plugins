# Duplicate Check — TC-8003

## Step 4 — Duplicate, Sibling, and Overlap Check

### JQL Search

Search for sibling Vulnerability issues with the same CVE label:

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8003
```

**Results: 1 sibling found.**

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|------------------|---------------|
| TC-7999 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

### Stream Classification

- TC-8003 stream suffix: `[rhtpa-2.2]` --> stream **2.2.x**
- TC-7999 stream suffix: `[rhtpa-2.2]` --> stream **2.2.x**
- Classification: **Same-stream sibling**

### 4.1 — Same-Stream Duplicate Analysis

TC-7999 is a same-stream sibling of TC-8003:

- Both issues track **CVE-2026-31812** (quinn-proto)
- Both issues are scoped to **stream 2.2.x** (suffix `[rhtpa-2.2]`)
- TC-7999 is already **In Progress** with Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1
- TC-8003 is **New** with Affects Versions: RHTPA 2.2.0

TC-7999 already covers the same CVE in the same stream, and its Affects Versions (RHTPA 2.2.0, RHTPA 2.2.1) are a superset of TC-8003's (RHTPA 2.2.0). TC-7999 is already actively being worked (In Progress status).

**Recommendation: Close TC-8003 as Duplicate of TC-7999.**

Per Step 4.1 of the triage-security skill:

> If a same-stream sibling exists and is open or in progress:
> - Recommendation: Close the current issue as Duplicate.

### Proposed Jira Actions (require engineer confirmation)

1. **Add comment** to TC-8003:
   > "Duplicate of TC-7999 -- same CVE (CVE-2026-31812) tracked for the same stream 2.2.x [rhtpa-2.2]. Version impact analysis confirms overlap. TC-7999 is already In Progress with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1]."

2. **Transition** TC-8003 to Closed with resolution **"Duplicate"**.

3. **Assign** TC-8003 to the current user.

### 4.2 — Cross-Stream Coordination

Not applicable. No different-stream siblings were found. The only sibling (TC-7999) is in the same stream.

### 4.3 — Cross-CVE Overlap Detection

Skipped. The Upstream Affected Component custom field is not configured in Security Configuration, so cross-CVE overlap detection cannot be performed.

### 4.4 — Preemptive Task Reconciliation

Not applicable. The issue is being closed as a duplicate, so no remediation tasks will be created. Preemptive task reconciliation is only relevant when proceeding to Step 8 (remediation).
