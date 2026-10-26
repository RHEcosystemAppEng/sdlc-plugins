# Duplicate Check — TC-8003

## Step 4 — Duplicate, Sibling, Overlap, and Reconciliation Check

### JQL Search for Sibling Issues

Query (simulated):
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8003
```

**Result**: 1 sibling issue found.

### Sibling Analysis

| Issue | Summary | Stream Suffix | Status | Labels | Affects Versions |
|-------|---------|---------------|--------|--------|------------------|
| TC-7999 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 |
| TC-8003 (current) | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | [rhtpa-2.2] | New | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0 |

### Classification

**TC-7999 is a same-stream sibling** of TC-8003:
- Both have the same CVE label: `CVE-2026-31812`
- Both have the same stream suffix: `[rhtpa-2.2]` (mapping to the 2.2.x stream)
- Both target the same component: `pscomponent:org/rhtpa-server`

Per Step 4.1 of the triage-security skill, when a same-stream sibling exists and is open or in progress, the current issue should be classified as a **duplicate**.

### Step 4.1 — Same-Stream Duplicate Detection

TC-7999 is already **In Progress**, meaning someone is actively working on triaging/remediating this CVE for the 2.2.x stream. TC-8003 is a duplicate entry for the same CVE in the same stream.

**Recommendation: Close TC-8003 as Duplicate of TC-7999.**

### Proposed Actions (would require engineer confirmation in interactive mode)

1. **Add comment to TC-8003**:
   > "Duplicate of TC-7999 -- same CVE (CVE-2026-31812) tracked for the same stream [rhtpa-2.2]. TC-7999 is already In Progress with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1]. Version impact analysis confirms overlap: both issues cover the 2.2.x stream where versions 2.2.0, 2.2.1, and 2.2.2 ship vulnerable quinn-proto versions (0.11.9 and 0.11.12, both below the fix threshold of 0.11.14)."

2. **Transition TC-8003 to Closed** with resolution "Duplicate".

3. **Note on Affects Versions**: TC-7999 already has Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1], which partially covers the affected versions. RHTPA 2.2.2 (retag of 2.2.1) is also affected but may not be registered in Jira. This correction should be applied to TC-7999 (the surviving issue), not TC-8003.

### No Further Steps Required

Because TC-8003 is a duplicate, the following steps are skipped:
- **Step 5 (Version Lifecycle Check)** — not needed for a duplicate
- **Step 6 (Already Fixed Check)** — not needed for a duplicate
- **Step 7 (Concurrent Triage Detection)** — not needed for a duplicate
- **Step 7.5 (Release Jira Orchestration)** — not needed for a duplicate
- **Step 8 (Remediation)** — TC-7999 handles remediation for this CVE/stream
