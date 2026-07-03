# Triage Outcome -- TC-8003

## Decision: Close as Duplicate

TC-8003 should be **closed as Duplicate** of TC-7999.

## Rationale

TC-8003 (CVE-2026-31812, quinn-proto panic on large stream counts, stream [rhtpa-2.2]) is a duplicate of TC-7999, which tracks the same CVE for the same version stream and is already In Progress.

### Version Impact Summary

The version impact analysis for CVE-2026-31812 (quinn-proto < 0.11.14) within the 2.2.x stream:

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | fixed version |
| 2.2.4 | 0.11.14 | NO | fixed version |

### Duplicate Evidence

| Criterion | TC-8003 | TC-7999 |
|-----------|---------|---------|
| CVE | CVE-2026-31812 | CVE-2026-31812 |
| Stream suffix | [rhtpa-2.2] | [rhtpa-2.2] |
| Status | New | In Progress |
| Affects Versions | RHTPA 2.2.0 | RHTPA 2.2.0, RHTPA 2.2.1 |

TC-7999 is the active tracking issue. It is already In Progress and has a more complete Affects Versions set (includes both RHTPA 2.2.0 and RHTPA 2.2.1). No new remediation tasks are needed from TC-8003.

### Cross-Stream Note

The 2.1.x stream is also affected (versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9). However, since TC-8003 is scoped to stream 2.2.x by its summary suffix and is being closed as a duplicate, cross-stream remediation for 2.1.x is not in scope for this triage. Any 2.1.x remediation would be handled through a separate CVE Jira for that stream, or through Case B (cross-stream proactive remediation) on TC-7999.

## Proposed Jira Actions

1. **Assign** TC-8003 to the current user
2. **Transition** TC-8003 from New to Assigned
3. **Add comment** to TC-8003:
   > Duplicate of TC-7999 -- same CVE (CVE-2026-31812) tracked for the same stream [rhtpa-2.2]. Version impact analysis confirms overlap. TC-7999 is already In Progress with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1].
4. **Transition** TC-8003 to Closed with resolution "Duplicate"
5. **Add label** `ai-cve-triaged` to TC-8003

## Steps Not Executed

The following steps were short-circuited because the issue is a duplicate:

- **Step 5 (Version Lifecycle Check)**: Not needed -- duplicate closure takes precedence
- **Step 6 (Already Fixed Check)**: Not needed -- duplicate closure takes precedence
- **Step 7 (Concurrent Triage Detection)**: Not needed -- no remediation tasks will be created
- **Step 8 (Remediation)**: Not needed -- TC-7999 already tracks remediation for this CVE and stream
