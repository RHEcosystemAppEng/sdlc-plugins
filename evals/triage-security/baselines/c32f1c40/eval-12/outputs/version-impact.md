# Step 2 — Version Impact Analysis

## Fix Threshold

Using the **enriched fix threshold from Step 1.5**: h2 < **0.4.8** (affected range)

This threshold was obtained from external CVE data enrichment (MITRE CVE API and OSV.dev, in agreement). The Jira description's imprecise "versions prior to the fix" is NOT used for comparisons.

## Version Impact Table

Version Impact for CVE-2026-48901 (h2 < 0.4.8):

| Version | Stream | Tag | h2 version | Affected? | Notes |
|---------|--------|-----|------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.4.8 | NO | 0.4.8 is not < 0.4.8 |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.4.8 | NO | 0.4.8 is not < 0.4.8 |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

## Stream-scoped Summary

This issue is scoped to **stream 2.2.x** (from summary suffix `[rhtpa-2.2]`).

- **2.2.x stream**: All versions (2.2.0 through 2.2.4) ship h2 >= 0.4.8, which is outside the affected range. **No 2.2.x versions are affected.**
- **2.1.x stream** (outside issue scope): Both versions (2.1.0 and 2.1.1) ship h2 0.4.5, which IS within the affected range (< 0.4.8). These versions are affected but belong to a different stream.

## Dependency Chain Context

```
Dependency chain for h2 (Cargo):
  backend (workspace) -> h2
  Type: direct dependency (present in Cargo.lock)
  Profile: production (h2 is a runtime dependency)

Note: h2 versions were extracted from Cargo.lock at pinned commits
from the supportability matrix for each version.
```

## Key Observation

The enriched fix threshold (0.4.8) from Step 1.5 was essential for this analysis. Without external enrichment, the Jira description's imprecise "versions prior to the fix" would not have allowed version impact comparisons. The MITRE CVE API's `lessThan: "0.4.8"` and OSV.dev's `fixed: "0.4.8"` provided the machine-readable constraint needed for precise version comparison.
