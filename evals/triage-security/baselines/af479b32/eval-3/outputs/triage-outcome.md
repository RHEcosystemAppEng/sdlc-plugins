# Triage Outcome -- TC-8003

## Decision: Close as Duplicate of TC-7999

### Rationale

TC-8003 is a **same-stream duplicate** of TC-7999. Both issues track the same vulnerability (CVE-2026-31812 in quinn-proto) for the same product stream (2.2.x, identified by the `[rhtpa-2.2]` suffix in both summaries).

TC-7999 is already **In Progress** with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1], which is a superset of TC-8003's Affects Versions [RHTPA 2.2.0]. All triage and remediation work for this CVE in stream 2.2.x is already being handled through TC-7999.

Per Step 4.1 of the triage-security skill, when a same-stream sibling exists and is open or in progress, the current issue should be closed as Duplicate.

### Proposed Jira Actions

The following Jira mutations would be performed (each requiring engineer confirmation):

1. **Add comment to TC-8003:**
   > Duplicate of TC-7999 -- same CVE (CVE-2026-31812) tracked for the same stream [rhtpa-2.2]. Version impact analysis confirms overlap. TC-7999 is already In Progress with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1].

2. **Transition TC-8003** to Closed with resolution **Duplicate**.

3. **Assign TC-8003** to current user.

4. **Add `ai-cve-triaged` label** to TC-8003.

### Steps Skipped Due to Duplicate Closure

The following steps are not applicable because the issue is being closed as a duplicate:

- **Step 3 (Affects Versions Correction)**: Not needed -- the duplicate issue TC-7999 already has the correct, broader Affects Versions.
- **Step 5 (Version Lifecycle Check)**: Not needed -- TC-7999's triage handles lifecycle checks.
- **Step 6 (Already Fixed Check)**: Not needed -- closure is due to duplication, not fix status.
- **Step 7 (Concurrent Triage Detection)**: Not needed -- no remediation tasks will be created.
- **Step 8 (Remediation)**: Not needed -- remediation is handled through TC-7999.

### Version Impact Summary (for reference)

Although TC-8003 is a duplicate, the version impact analysis was completed to confirm the overlap:

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | Outside TC-8003's scope |
| 2.1.1 | 2.1.x | 0.11.9 | YES | Outside TC-8003's scope |
| 2.2.0 | 2.2.x | 0.11.9 | YES | Covered by TC-7999 |
| 2.2.1 | 2.2.x | 0.11.12 | YES | Covered by TC-7999 |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1; Covered by TC-7999 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | Fixed |
| 2.2.4 | 2.2.x | 0.11.14 | NO | Fixed |

The fix was introduced in version 2.2.3 (build 0.4.11), which ships quinn-proto 0.11.14 (the fixed version). Versions 2.2.0 through 2.2.2 are affected and are already tracked by TC-7999.

### Cross-Stream Note

Stream 2.1.x (versions 2.1.0 and 2.1.1) is also affected by CVE-2026-31812 (quinn-proto 0.11.9 < 0.11.14). However, this is outside TC-8003's scope (which is scoped to 2.2.x). The 2.1.x stream would require its own CVE Jira or would be handled by TC-7999's triage if TC-7999 performs cross-stream impact analysis (Step 8, Case B).
