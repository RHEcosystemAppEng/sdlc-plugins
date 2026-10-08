# Duplicate Check (Step 4) -- TC-8003

## JQL Sibling Search

Query (simulated):
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8003
```

Results: **1 sibling found**

## Sibling Analysis

| Issue | Summary | Stream Suffix | Status | Affects Versions |
|-------|---------|---------------|--------|------------------|
| TC-7999 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | [rhtpa-2.2] | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |
| TC-8003 (current) | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | [rhtpa-2.2] | New | RHTPA 2.2.0 |

## Classification

### Step 4.1 -- Same-stream duplicate check

TC-7999 has the **same stream suffix** `[rhtpa-2.2]` as TC-8003. Both issues
track the same CVE (CVE-2026-31812) for the same version stream (2.2.x).

TC-7999 is currently **In Progress**, meaning it is actively being worked on.
Its Affects Versions `[RHTPA 2.2.0, RHTPA 2.2.1]` is a superset of TC-8003's
`[RHTPA 2.2.0]`, confirming it already covers the versions identified in TC-8003.

**Classification: Same-stream duplicate.**

Per Step 4.1 of the triage-security skill:

> "If a same-stream sibling exists and is open or in progress:
> Recommendation: Close the current issue as Duplicate."

### Step 4.2 -- Cross-stream coordination

Not applicable. The only sibling found (TC-7999) is a same-stream sibling, not a
cross-stream companion. No different-stream siblings were found.

### Step 4.3 -- Cross-CVE overlap detection

Skipped. The Upstream Affected Component custom field, PS Component custom field,
and Stream custom field are not configured in the project's Security Configuration.

### Step 4.4 -- Preemptive task reconciliation

Skipped. The issue is being closed as a duplicate, so no remediation tasks will
be created for this issue. Preemptive task reconciliation is not applicable.

## Recommendation

**Close TC-8003 as Duplicate of TC-7999.**

TC-7999 is the authoritative tracker for CVE-2026-31812 in the 2.2.x stream.
It is already In Progress with the correct Affects Versions (RHTPA 2.2.0,
RHTPA 2.2.1), which is actually more complete than TC-8003's PSIRT-assigned
version list (RHTPA 2.2.0 only).

### Proposed Jira Actions (require engineer confirmation)

1. Add comment to TC-8003:
   "Duplicate of TC-7999 -- same CVE (CVE-2026-31812) tracked for the same
   stream [rhtpa-2.2]. TC-7999 is already In Progress with Affects Versions
   [RHTPA 2.2.0, RHTPA 2.2.1]. Version impact analysis confirms overlap."

2. Transition TC-8003 to Closed with resolution "Duplicate".

3. Assign TC-8003 to current user.
