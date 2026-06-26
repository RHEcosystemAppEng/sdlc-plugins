# Step 2 -- Version Impact Analysis

## Enriched Fix Threshold

Using the cross-validated fix threshold from Step 1.5: **h2 < 0.4.8 is affected** (fix version: 0.4.8).

## 2.2.x Stream (Scoped -- issue stream)

The issue TC-8030 is scoped to the 2.2.x stream via the `[rhtpa-2.2]` suffix.

### Version Impact Table

Version Impact for CVE-2026-48901 (h2 < 0.4.8):

| Version | Build Tag | h2 version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.4.8 | NO | ships h2 0.4.8 (= fix threshold) |
| 2.2.1 | v0.4.8 | 0.4.8 | NO | ships h2 0.4.8 (= fix threshold) |
| 2.2.2 | v0.4.8 | 0.4.8 | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.4.9 | NO | ships h2 0.4.9 (> fix threshold) |
| 2.2.4 | v0.4.12 | 0.4.9 | NO | ships h2 0.4.9 (> fix threshold) |

**Result: No versions in the 2.2.x stream are affected.** All versions ship h2 >= 0.4.8.

## 2.1.x Stream (Cross-stream analysis)

Although the issue is scoped to 2.2.x, cross-stream analysis covers all configured streams.

| Version | Build Tag | h2 version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.4.5 | YES | ships h2 0.4.5 (< 0.4.8 fix threshold) |
| 2.1.1 | v0.3.12 | 0.4.5 | YES | ships h2 0.4.5 (< 0.4.8 fix threshold) |

**Result: All versions in the 2.1.x stream ARE affected.** Both ship h2 0.4.5 which is below the fix threshold of 0.4.8.

## Combined Version Impact Summary

| Stream | Versions Affected | Versions Not Affected |
|--------|-------------------|-----------------------|
| 2.2.x (scoped) | None | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 |
| 2.1.x (cross-stream) | 2.1.0, 2.1.1 | None |

## Triage Outcome

- **Scoped stream (2.2.x)**: No supported versions are affected. This maps to **Case C** -- close as Not a Bug.
- **Cross-stream (2.1.x)**: All versions are affected. This maps to **Case B** -- cross-stream impact requiring proactive remediation or a companion CVE Jira for the 2.1.x stream.
