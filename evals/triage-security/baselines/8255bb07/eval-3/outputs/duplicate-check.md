# Duplicate Check -- TC-8003

## Step 4 -- Duplicate, Sibling, and Overlap Check

### JQL Search

A JQL search for sibling Vulnerability issues with the same CVE label was performed:

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8003
```

**Result**: 1 sibling issue found.

### Sibling Issue Details

| Field | TC-7999 (Sibling) | TC-8003 (Current) |
|-------|-------------------|-------------------|
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Status | In Progress | New |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server | CVE-2026-31812, pscomponent:org/rhtpa-server |
| Stream suffix | [rhtpa-2.2] | [rhtpa-2.2] |
| Affects Versions | RHTPA 2.2.0, RHTPA 2.2.1 | RHTPA 2.2.0 |

### Step 4.1 -- Same-Stream Duplicate Classification

TC-7999 has the **same stream suffix** `[rhtpa-2.2]` as TC-8003. Both issues track CVE-2026-31812 for the 2.2.x stream.

Per the triage-security procedure (Step 4.1): when a same-stream sibling exists and is open or in progress, the current issue should be classified as a **duplicate**.

**Classification**: TC-8003 is a **same-stream duplicate** of TC-7999.

**Key evidence**:
1. Same CVE: CVE-2026-31812
2. Same stream suffix: [rhtpa-2.2]
3. Same component: pscomponent:org/rhtpa-server
4. TC-7999 is already **In Progress** -- active triage/remediation is underway
5. TC-7999 already has broader Affects Versions coverage (RHTPA 2.2.0, RHTPA 2.2.1) compared to TC-8003 (RHTPA 2.2.0 only)

### Affects Versions Overlap

TC-7999 already carries Affects Versions `RHTPA 2.2.0, RHTPA 2.2.1`. Based on the version impact analysis (see data-extraction.md), RHTPA 2.2.2 is also affected but this is a retag of 2.2.1. The existing sibling TC-7999 covers the primary affected versions. Any Affects Versions correction (adding RHTPA 2.2.2) should be applied to TC-7999, not TC-8003.

### Step 4.3 -- Cross-CVE Overlap Detection

Skipped. The Upstream Affected Component custom field, PS Component custom field, and Stream custom field are not configured in the Security Configuration. Per the skill procedure, Step 4.3 is skipped entirely when these fields are not configured.

### Step 4.4 -- Preemptive Task Reconciliation

Not applicable. The issue is being recommended for closure as duplicate, so preemptive task reconciliation is not needed.

### Recommendation

**Close TC-8003 as Duplicate of TC-7999.**

TC-7999 is the authoritative tracker for CVE-2026-31812 in the 2.2.x stream and is already In Progress. Continuing triage on TC-8003 would produce duplicate remediation tasks and fragment tracking.
