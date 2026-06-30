# Duplicate Check — TC-8003

## Step 4 — Duplicate, Sibling, Overlap, and Reconciliation Check

### JQL Search Performed

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8003
```

### Search Results

One sibling issue found:

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|------------------|---------------|
| TC-7999 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

### Step 4.1 — Same-Stream Duplicate Classification

**Current issue (TC-8003):** stream suffix `[rhtpa-2.2]` maps to stream **2.2.x**
**Sibling issue (TC-7999):** stream suffix `[rhtpa-2.2]` maps to stream **2.2.x**

Classification: **Same-stream sibling** — both TC-8003 and TC-7999 track CVE-2026-31812 for the same stream (2.2.x).

TC-7999 is already **In Progress**, meaning triage and remediation work is actively underway for this CVE in the 2.2.x stream. TC-7999 already has the correct Affects Versions (RHTPA 2.2.0, RHTPA 2.2.1), which matches what the version impact analysis would produce for affected 2.2.x versions (2.2.0, 2.2.1, 2.2.2 are affected; 2.2.2 is a retag of 2.2.1).

### Duplicate Determination

TC-8003 is a **duplicate** of TC-7999:

1. Both issues track the same CVE (CVE-2026-31812)
2. Both issues are scoped to the same stream (2.2.x, suffix `[rhtpa-2.2]`)
3. TC-7999 is already In Progress with Affects Versions RHTPA 2.2.0 and RHTPA 2.2.1
4. TC-8003 has a subset of those Affects Versions (only RHTPA 2.2.0)
5. There is no reason to maintain two Vulnerability issues for the same CVE in the same stream

### Recommendation

**Close TC-8003 as Duplicate of TC-7999.**

Proposed actions (require engineer confirmation before execution):

1. **Add comment to TC-8003:**
   > Duplicate of TC-7999 -- same CVE (CVE-2026-31812) tracked for the same stream [rhtpa-2.2]. TC-7999 is already In Progress with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1]. Version impact analysis confirms overlap: both issues cover the 2.2.x stream where quinn-proto < 0.11.14 is affected.

2. **Transition TC-8003** to Closed with resolution "Duplicate"

3. **Assign TC-8003** to the current user

4. **Add label** `ai-cve-triaged` to TC-8003

### Step 4.2 — Cross-Stream Coordination

Not applicable. TC-7999 is a same-stream sibling, not a cross-stream companion. No different-stream siblings were found in the JQL results for this CVE.

### Step 4.3 — Cross-CVE Overlap Detection

Skipped. The Upstream Affected Component custom field, PS Component custom field, and Stream custom field are not configured in Security Configuration. Cross-CVE overlap detection requires these fields.

### Step 4.4 — Preemptive Task Reconciliation

Skipped. The issue is being closed as a duplicate — no remediation tasks will be created, so preemptive task reconciliation is not needed.
