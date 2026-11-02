# Step 2 — Version Impact Analysis for CVE-2026-48901

## Fix Threshold

Using enriched fix threshold from Step 1.5: **h2 < 0.4.8** (versions below 0.4.8 are affected).

This threshold was obtained from cross-validated MITRE CVE API and OSV.dev data, replacing the imprecise Jira description ("versions prior to the fix").

## Version Impact Table (2.2.x stream — scoped)

| Version | Build Tag | h2 version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.2.0 | `v0.4.5` | 0.4.8 | **NO** | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.1 | `v0.4.8` | 0.4.8 | **NO** | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.2 | `v0.4.9` | — | **NO** | retag of 2.2.1, same as 2.2.1 |
| 2.2.3 | `v0.4.11` | 0.4.9 | **NO** | 0.4.9 >= 0.4.8 (above fix threshold) |
| 2.2.4 | `v0.4.12` | 0.4.9 | **NO** | 0.4.9 >= 0.4.8 (above fix threshold) |

## Cross-Stream Reference (2.1.x stream — outside scope)

| Version | Build Tag | h2 version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.1.0 | `v0.3.8` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.1 | `v0.3.12` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |

## Summary

**Within the scoped 2.2.x stream**: No supported versions are affected. All versions ship h2 >= 0.4.8, which is at or above the enriched fix threshold.

**Cross-stream note**: The 2.1.x stream IS affected (h2 = 0.4.5 < 0.4.8), but this issue is scoped to the 2.2.x stream per the `[rhtpa-2.2]` suffix. The 2.1.x impact would be tracked by a separate CVE Jira for that stream.

## Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) → h2
  Type: direct dependency (present in Cargo.lock for all versions)
  Profile: production (h2 is a runtime HTTP/2 implementation dependency)
```

No affected versions exist in the scoped 2.2.x stream, so remediation is not required for this stream.
