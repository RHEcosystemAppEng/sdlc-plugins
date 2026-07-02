# Triage Outcome -- TC-8003

## Decision: Close as Duplicate

TC-8003 should be **closed as Duplicate** of TC-7999.

## Rationale

### Same CVE, Same Stream

TC-8003 and TC-7999 both track CVE-2026-31812 (quinn-proto panic on large stream counts) for the same product stream `[rhtpa-2.2]` (2.2.x). PSIRT created two Vulnerability issues for the same CVE targeting the same stream, which is a duplicate.

### TC-7999 Is Already In Progress

TC-7999 is already in **In Progress** status, meaning an engineer is actively working on the triage or remediation. Its Affects Versions are set to [RHTPA 2.2.0, RHTPA 2.2.1], which correctly reflects the versions that ship vulnerable quinn-proto versions (0.11.9 and 0.11.12, both below the fix threshold of 0.11.14).

### Version Impact Confirmation

The version impact analysis confirms the overlap between the two issues:

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| RHTPA 2.2.0 | 0.11.9 | YES |
| RHTPA 2.2.1 | 0.11.12 | YES |
| RHTPA 2.2.2 | (retag of 2.2.1) | YES |
| RHTPA 2.2.3 | 0.11.14 | NO (fixed) |
| RHTPA 2.2.4 | 0.11.14 | NO (fixed) |

TC-7999 already covers RHTPA 2.2.0 and RHTPA 2.2.1 in its Affects Versions. There is no version-level gap that TC-8003 would fill.

### Cross-Stream Note

The 2.1.x stream is also affected (versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9), but this is outside the scope of both TC-8003 and TC-7999 (both scoped to [rhtpa-2.2]). The 2.1.x stream would need its own CVE Jira from PSIRT or would be handled via cross-stream proactive remediation (Case B) during TC-7999's triage.

## Steps Skipped Due to Duplicate Closure

The following steps are not executed because the issue is being closed as duplicate:

- **Step 5 (Version Lifecycle Check)**: Not needed -- TC-7999 handles lifecycle assessment.
- **Step 6 (Already Fixed Check)**: Not needed -- TC-7999 is the active tracker.
- **Step 7 (Concurrent Triage Detection)**: Not needed -- no remediation tasks will be created.
- **Step 8 (Remediation)**: Not needed -- TC-7999 owns remediation for this CVE in the 2.2.x stream.

## Proposed Jira Mutations (pending engineer confirmation)

1. **Assign** TC-8003 to the current user.
2. **Add comment** to TC-8003:
   > Duplicate of TC-7999 -- same CVE (CVE-2026-31812) tracked for the same stream [rhtpa-2.2]. Version impact analysis confirms overlap. TC-7999 is already In Progress with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1].
3. **Transition** TC-8003 to Closed with resolution "Duplicate".
4. **Add label** `ai-cve-triaged` to TC-8003.
