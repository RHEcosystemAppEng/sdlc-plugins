# Step 2 -- Version Impact Analysis

## Enriched Fix Threshold

Using the cross-validated fix threshold from Step 1.5: **h2 < 0.4.8** is affected.

## Version Impact Table

Version Impact for CVE-2026-48901 (h2 < 0.4.8):

### Stream 2.2.x (issue-scoped stream)

| Version | Build Tag | h2 version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.4.8 | NO | ships fixed version (0.4.8 >= 0.4.8) |
| 2.2.1 | v0.4.8 | 0.4.8 | NO | ships fixed version (0.4.8 >= 0.4.8) |
| 2.2.2 | v0.4.8 | 0.4.8 | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.4.9 | NO | ships fixed version (0.4.9 >= 0.4.8) |
| 2.2.4 | v0.4.12 | 0.4.9 | NO | ships fixed version (0.4.9 >= 0.4.8) |

**Result for 2.2.x: NO versions affected.** All versions in the 2.2.x stream ship h2 >= 0.4.8, which is at or above the fix threshold.

### Stream 2.1.x (cross-stream analysis)

| Version | Build Tag | h2 version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.1.1 | v0.3.12 | 0.4.5 | YES | 0.4.5 < 0.4.8 |

**Result for 2.1.x: ALL versions affected.** Both versions in the 2.1.x stream ship h2 0.4.5, which is below the fix threshold of 0.4.8.

## Summary

| Stream | Versions Affected | Versions Not Affected | Overall |
|--------|------------------|-----------------------|---------|
| 2.2.x (scoped) | 0 | 5 (including retag) | NOT AFFECTED |
| 2.1.x (cross-stream) | 2 | 0 | AFFECTED |

## Triage Outcome

**Scoped stream (2.2.x)**: No supported versions ship a vulnerable version of h2. All versions in the 2.2.x stream ship h2 0.4.8 or later, which is at or above the fix threshold. This is **Case C: Close as Not a Bug**.

**Cross-stream impact (2.1.x)**: Both versions (2.1.0 and 2.1.1) ship h2 0.4.5, which is within the affected range. This is **Case A: Cross-stream impact**. The 2.1.x stream requires remediation, tracked through its own CVE Jira or preemptive remediation tasks.

## PSIRT Affects Versions Correction

The current Affects Versions field lists "RHTPA 2.2.0". Since no versions in the 2.2.x stream are actually affected, the Affects Versions should be corrected:
- **Remove**: RHTPA 2.2.0 (not affected -- ships h2 0.4.8)
- The vulnerability affects the 2.1.x stream instead, but that is outside this issue's scope.
