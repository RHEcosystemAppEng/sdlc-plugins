# Triage Outcome -- TC-8003

## Decision: Close as Duplicate

TC-8003 should be **closed as Duplicate** of TC-7999.

## Rationale

### 1. Same CVE, same stream

Both TC-8003 and TC-7999 track CVE-2026-31812 (quinn-proto panic on large
stream counts) for the same version stream: `[rhtpa-2.2]` (the 2.2.x stream).
PSIRT created two separate Vulnerability issues for the same CVE in the same
stream, which is a duplication.

### 2. TC-7999 is already In Progress

TC-7999 has status **In Progress**, meaning an engineer is already actively
triaging or remediating this vulnerability. TC-8003 is still in **New** status
and has not been worked on.

### 3. TC-7999 has more complete Affects Versions

TC-7999 already carries Affects Versions `[RHTPA 2.2.0, RHTPA 2.2.1]`, which
correctly reflects the lock file analysis showing quinn-proto < 0.11.14 in
versions 2.2.0 (ships 0.11.9) and 2.2.1 (ships 0.11.12).

TC-8003 only has `[RHTPA 2.2.0]`, which is incomplete -- it is missing RHTPA
2.2.1. This further confirms TC-7999 is the more complete tracker.

### 4. Version impact confirms no unique coverage

The version impact analysis for the 2.2.x stream shows:

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.2.0 | 0.11.9 | YES |
| 2.2.1 | 0.11.12 | YES |
| 2.2.2 | (retag of 2.2.1) | YES |
| 2.2.3 | 0.11.14 | NO |
| 2.2.4 | 0.11.14 | NO |

All affected versions (2.2.0, 2.2.1, 2.2.2) are already covered by TC-7999's
Affects Versions. TC-8003 provides no additional version coverage.

### 5. Cross-stream note

The 2.1.x stream is also affected (versions 2.1.0 and 2.1.1 both ship
quinn-proto 0.11.9), but this is outside the scope of both TC-8003 and TC-7999
(both scoped to [rhtpa-2.2]). The 2.1.x stream would need its own CVE Jira
from PSIRT or a cross-stream impact assessment from TC-7999's triage.

## Triage Actions Summary

| Step | Action | Status |
|------|--------|--------|
| Step 0 | Validate configuration | Pass -- Security Configuration present |
| Step 0.3 | Matrix staleness check | Matrix dated 2026-06-28 (within 14 days of eval date) |
| Step 1 | Data extraction | Complete -- CVE-2026-31812, quinn-proto < 0.11.14 |
| Step 2 | Version impact analysis | Complete -- 2.2.0, 2.2.1, 2.2.2 affected; 2.2.3, 2.2.4 not affected |
| Step 3 | Affects Versions correction | Skipped -- closing as duplicate |
| Step 4 | Duplicate check | **TC-7999 identified as same-stream duplicate (In Progress)** |
| Step 4.1 | Same-stream duplicate | **Match found -- close TC-8003** |
| Step 5 | Version lifecycle check | Skipped -- closing as duplicate |
| Step 6 | Already fixed check | Skipped -- closing as duplicate |
| Step 7 | Concurrent triage detection | Skipped -- closing as duplicate |
| Step 7.5 | Release Jira orchestration | Skipped -- closing as duplicate |
| Step 8 | Remediation | **Not needed -- duplicate of TC-7999** |

## Proposed Jira Mutations (pending engineer confirmation)

1. **Comment on TC-8003**: "Duplicate of TC-7999 -- same CVE (CVE-2026-31812) tracked
   for the same stream [rhtpa-2.2]. TC-7999 is already In Progress with Affects
   Versions [RHTPA 2.2.0, RHTPA 2.2.1]. Version impact analysis confirms complete
   overlap."

2. **Transition TC-8003** to Closed with resolution "Duplicate".

3. **Assign TC-8003** to current user.

No remediation tasks are created. No `ai-cve-triaged` label is added (the issue
is closed as duplicate, not triaged independently).
