# Triage Outcome: TC-8003

## Decision: Close as Duplicate

TC-8003 (CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]) is a **duplicate** of TC-7999, which tracks the same CVE for the same version stream and is already In Progress.

## Rationale

1. **Same CVE**: Both TC-8003 and TC-7999 carry the label CVE-2026-31812.
2. **Same stream**: Both issues have the stream suffix `[rhtpa-2.2]`, scoping them to the 2.2.x version stream.
3. **TC-7999 is already active**: TC-7999 has status "In Progress", meaning an engineer is already triaging or remediating this vulnerability for the 2.2.x stream.
4. **TC-7999 has broader Affects Versions**: TC-7999 lists RHTPA 2.2.0 and RHTPA 2.2.1, while TC-8003 only lists RHTPA 2.2.0. The version impact analysis confirms both versions are affected (quinn-proto 0.11.9 and 0.11.12, both below the 0.11.14 fix threshold), so TC-7999's Affects Versions are more complete.
5. **No remediation tasks needed from TC-8003**: Since TC-7999 is already tracking remediation for this CVE in the 2.2.x stream, creating additional remediation tasks from TC-8003 would produce duplicates.

## Version Impact Summary

For reference, the version impact analysis for the 2.2.x stream (the issue-scoped stream) shows:

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | fixed version |
| 2.2.4 | 0.11.14 | NO | fixed version |

The fix was introduced in version 2.2.3 (build tag v0.4.11), which ships quinn-proto 0.11.14 (the fixed version).

## Proposed Jira Actions

All actions require engineer confirmation per skill guardrails.

1. **Add comment to TC-8003**:
   > Duplicate of TC-7999 -- same CVE (CVE-2026-31812) tracked for the same stream [rhtpa-2.2]. Version impact analysis confirms overlap. TC-7999 is already In Progress with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1].

2. **Transition TC-8003** to Closed with resolution "Duplicate".

3. **Assign TC-8003** to the current user.

4. **Add label** `ai-cve-triaged` to TC-8003 to mark it as triaged.

## Steps Not Executed

The following steps were short-circuited by the duplicate finding:

- **Step 3 (Affects Versions Correction)**: Not needed -- the issue is being closed as duplicate.
- **Steps 4.2-4.4 (Cross-stream, Overlap, Reconciliation)**: Not applicable after duplicate classification.
- **Step 5 (Version Lifecycle Check)**: Not needed -- duplicate closure does not require lifecycle verification.
- **Step 6 (Already Fixed Check)**: Not needed -- duplicate closure takes precedence.
- **Step 7 (Concurrent Triage Detection)**: Not needed -- no remediation tasks will be created.
- **Step 8 (Remediation)**: Not needed -- TC-7999 owns remediation for this CVE in the 2.2.x stream.

## Cross-Stream Note

The 2.1.x stream is also affected (all versions ship quinn-proto 0.11.9), but this is outside the scope of TC-8003 (which is scoped to 2.2.x). Cross-stream impact for the 2.1.x stream would be handled by whichever issue (TC-7999 or a separate PSIRT-created issue) actively proceeds through triage for the 2.2.x stream.
