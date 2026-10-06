# Triage Outcome: TC-8003

## Decision: Close as Duplicate

**TC-8003 should be closed as a Duplicate of TC-7999.**

## Rationale

TC-8003 (CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]) is a duplicate of TC-7999, which tracks the identical CVE in the identical version stream. The evidence is:

1. **Same CVE**: Both issues carry label `CVE-2026-31812`.
2. **Same stream**: Both issues have stream suffix `[rhtpa-2.2]`, mapping to the 2.2.x version stream.
3. **Same component**: Both issues carry label `pscomponent:org/rhtpa-server`.
4. **TC-7999 is already In Progress**: Active remediation work is underway on TC-7999.
5. **TC-7999 has broader coverage**: TC-7999 lists Affects Versions RHTPA 2.2.0 and RHTPA 2.2.1, while TC-8003 only lists RHTPA 2.2.0. The existing issue already covers all affected versions.

## Version Impact Summary

| Version | quinn-proto | Affected? | Covered by TC-7999? |
|---------|-------------|-----------|---------------------|
| RHTPA 2.2.0 | 0.11.9 | YES | YES |
| RHTPA 2.2.1 | 0.11.12 | YES | YES |
| RHTPA 2.2.2 | 0.11.12 (retag of 2.2.1) | YES | Not in Affects Versions but same stream |
| RHTPA 2.2.3 | 0.11.14 | NO (fixed) | N/A |
| RHTPA 2.2.4 | 0.11.14 | NO (fixed) | N/A |

All affected versions in the 2.2.x stream are already tracked by TC-7999. No remediation gap exists.

## Proposed Jira Mutations

All mutations require engineer confirmation per skill guardrails.

### 1. Close TC-8003 as Duplicate

- **Comment** on TC-8003:
  > Duplicate of TC-7999 -- same CVE (CVE-2026-31812) tracked for the same stream [rhtpa-2.2]. Version impact analysis confirms overlap: both issues cover quinn-proto vulnerability in RHTPA 2.2.0 and 2.2.1. TC-7999 is already In Progress with remediation underway.
  >
  > No new remediation tasks are needed -- TC-7999 handles all remediation for this CVE in the 2.2.x stream.

- **Transition**: TC-8003 to Closed, resolution = "Duplicate"
- **Assign**: TC-8003 to current user
- **Add label**: `ai-cve-triaged` to TC-8003

### 2. Post-triage summary comment

A summary comment would be added to TC-8003 documenting:
- The version impact table (quinn-proto versions across all 2.2.x releases)
- The Affects Versions status (TC-8003 had RHTPA 2.2.0 only; TC-7999 already covers RHTPA 2.2.0 and 2.2.1)
- The triage outcome: Closed as Duplicate of TC-7999
- @mention of the reporter (PSIRT analyst) for visibility

## Steps Not Reached

Because the issue is closed as Duplicate in Step 4, the following steps are not executed:

- **Step 5 (Version Lifecycle Check)**: Not needed -- no remediation action required on TC-8003.
- **Step 6 (Already Fixed Check)**: Not needed -- duplicate resolution takes precedence.
- **Step 7 (Concurrent Triage Detection)**: Not needed -- no remediation tasks will be created.
- **Step 8 (Remediation)**: Not needed -- TC-7999 handles all remediation.

## Cross-Stream Note

The 2.1.x stream (rhtpa-release.0.3.z) is also affected by CVE-2026-31812:
- RHTPA 2.1.0 ships quinn-proto 0.11.9 (affected)
- RHTPA 2.1.1 ships quinn-proto 0.11.9 (affected)

However, TC-8003 is scoped to [rhtpa-2.2] and is being closed as a duplicate, so no cross-stream action is taken from this issue. The 2.1.x stream would need its own CVE Jira (created by PSIRT) or proactive remediation from TC-7999's triage.
