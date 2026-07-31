# Triage Outcome — TC-8003

## Decision: Close as Duplicate

TC-8003 is a **duplicate** of **TC-7999**.

### Rationale

Both TC-8003 and TC-7999 track the same CVE (CVE-2026-31812) for the same product version stream (2.2.x, identified by the shared stream suffix `[rhtpa-2.2]`). TC-7999 is already **In Progress**, meaning an engineer is actively triaging or remediating the vulnerability. There is no need for a second issue to track the same CVE in the same stream.

### Proposed Jira Mutations

1. **Add comment** to TC-8003:
   > Duplicate of TC-7999 -- same CVE (CVE-2026-31812) tracked for the same stream [rhtpa-2.2]. TC-7999 is already In Progress with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1]. Version impact analysis confirms overlap. No separate remediation is needed for this issue.

2. **Transition** TC-8003 to **Closed** with resolution **Duplicate**.

3. **Assign** TC-8003 to the current user.

### What is NOT done

The following steps are **skipped** because duplicate detection short-circuits the triage flow:

- Step 4.2 (Cross-stream coordination) -- not applicable; this is a same-stream duplicate, not a cross-stream companion
- Step 4.3 (Cross-CVE overlap detection) -- skipped; issue is being closed as duplicate
- Step 4.4 (Preemptive task reconciliation) -- skipped; issue is being closed as duplicate
- Step 5 (Version Lifecycle Check) -- skipped; no remediation needed
- Step 6 (Already Fixed Check) -- skipped; no remediation needed
- Step 7 (Concurrent Triage Detection) -- skipped; no remediation tasks to create
- Step 8 (Remediation task creation) -- **NOT executed**; no remediation tasks are created because TC-7999 already handles remediation for this CVE in the 2.2.x stream

### Reference

- **Original issue**: TC-7999 (In Progress, Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1)
- **Duplicate issue**: TC-8003 (to be closed)
- **CVE**: CVE-2026-31812
- **Stream**: 2.2.x ([rhtpa-2.2])
- **Library**: quinn-proto (affected versions before 0.11.14, fixed in 0.11.14)
