# Triage Outcome: TC-8003

## Decision: Close as Duplicate of TC-7999

TC-8003 is a **duplicate** of TC-7999 and should be closed without creating any remediation tasks.

## Rationale

1. **Same CVE**: Both TC-8003 and TC-7999 track CVE-2026-31812 (quinn-proto panic on large stream counts).

2. **Same stream scope**: Both issues carry the summary suffix `[rhtpa-2.2]`, placing them in the 2.2.x version stream. PSIRT creates one Vulnerability issue per stream per CVE. Having two issues for the same CVE in the same stream is a duplicate, not a companion tracker.

3. **TC-7999 is already In Progress**: The sibling issue is actively being triaged or remediated. Work is already underway.

4. **TC-7999 has a more complete scope**: TC-7999 already lists Affects Versions as RHTPA 2.2.0 and RHTPA 2.2.1, which is a superset of TC-8003's Affects Versions (RHTPA 2.2.0 only). Version impact analysis from the security matrix confirms that versions 2.2.0 (quinn-proto 0.11.9) and 2.2.1 (quinn-proto 0.11.12) are affected, while 2.2.3+ ship the fixed version 0.11.14. TC-7999 already covers this correctly.

## Steps Not Executed (due to duplicate closure)

The following steps are skipped because the issue is closed as a duplicate:

- **Step 5 (Version Lifecycle Check)**: Not needed; TC-7999 will handle lifecycle verification.
- **Step 6 (Already Fixed Check)**: Not needed; TC-7999 will handle this.
- **Step 7 (Concurrent Triage Detection)**: Not needed; no remediation tasks will be created from TC-8003.
- **Step 7.5 (Release Jira Orchestration)**: Not needed; no remediation tasks to link.
- **Step 8 (Remediation)**: Not needed; TC-7999 owns remediation for CVE-2026-31812 in stream 2.2.x.

## Proposed Jira Mutations (all require engineer confirmation)

| # | Operation | Details |
|---|-----------|---------|
| 1 | Assign TC-8003 | Assign to current user |
| 2 | Transition TC-8003 | New -> Assigned (if transition available) |
| 3 | Add comment | "Duplicate of TC-7999 -- same CVE (CVE-2026-31812) tracked for the same stream 2.2.x [rhtpa-2.2]. TC-7999 is already In Progress with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1]. Version impact analysis confirms overlap." |
| 4 | Transition TC-8003 | Assigned -> Closed, resolution: Duplicate |
| 5 | Add label | `ai-cve-triaged` |

## Post-Triage Summary Comment

A post-triage summary comment would be posted to TC-8003 documenting:

- Version impact table (2.2.0: YES, 2.2.1: YES, 2.2.2: YES retag, 2.2.3: NO, 2.2.4: NO)
- Duplicate determination: same-stream sibling TC-7999 already In Progress
- Triage outcome: Closed as Duplicate
- No remediation tasks created (TC-7999 owns remediation)
- Cross-stream note: Stream 2.1.x (versions 2.1.0, 2.1.1) is also affected but is outside this issue's scope

## Version Impact Summary (for reference)

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | Outside issue scope |
| 2.1.1 | 2.1.x | 0.11.9 | YES | Outside issue scope |
| 2.2.0 | 2.2.x | 0.11.9 | YES | In scope, covered by TC-7999 |
| 2.2.1 | 2.2.x | 0.11.12 | YES | In scope, covered by TC-7999 |
| 2.2.2 | 2.2.x | (retag of 2.2.1) | YES | In scope, retag, covered by TC-7999 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | Fixed (>= 0.11.14) |
| 2.2.4 | 2.2.x | 0.11.14 | NO | Fixed (>= 0.11.14) |
