# Step 2 -- Version Impact Analysis

## Fix Threshold

Using the **enriched fix threshold from Step 1.5**: h2 < **0.4.8** (affected)

This threshold was obtained from external CVE databases (MITRE CVE API and OSV.dev), NOT from the imprecise Jira description which only stated "versions prior to the fix." Both external sources agreed on 0.4.8 as the fix boundary.

## Version Impact Table

Version Impact for CVE-2026-48901 (h2 < 0.4.8):

### 2.2.x Stream (in-scope per issue suffix [rhtpa-2.2])

| Version | Tag | h2 version | Affected? | Notes |
|---------|-----|-----------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.4.8 | NO | 0.4.8 >= 0.4.8 fix threshold |
| 2.2.1 | v0.4.8 | 0.4.8 | NO | 0.4.8 >= 0.4.8 fix threshold |
| 2.2.2 | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.4.9 | NO | 0.4.9 >= 0.4.8 fix threshold |
| 2.2.4 | v0.4.12 | 0.4.9 | NO | 0.4.9 >= 0.4.8 fix threshold |

**Result**: No versions in the 2.2.x stream are affected. All ship h2 >= 0.4.8.

### 2.1.x Stream (cross-stream, out of scope)

| Version | Tag | h2 version | Affected? | Notes |
|---------|-----|-----------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.4.5 | YES | 0.4.5 < 0.4.8 fix threshold |
| 2.1.1 | v0.3.12 | 0.4.5 | YES | 0.4.5 < 0.4.8 fix threshold |

**Result**: Both versions in the 2.1.x stream are affected. They ship h2 0.4.5 which is below the 0.4.8 fix threshold.

## Dependency Chain Context (Step 2.3.5)

For the affected 2.1.x versions (h2 0.4.5):

```
Dependency chain for h2:
  backend (workspace) -> h2
  Type: direct dependency (present in Cargo.lock)
  Profile: production (h2 is a runtime HTTP/2 implementation dependency)

Remediation: bump h2 to >= 0.4.8 in Cargo.toml
```

## Cross-Stream Impact Summary

| Stream | Versions Affected | h2 Versions Shipped | Status |
|--------|-------------------|---------------------|--------|
| 2.2.x (in-scope) | 0 of 5 | 0.4.8, 0.4.9 | NOT AFFECTED |
| 2.1.x (out of scope) | 2 of 2 | 0.4.5 | AFFECTED |

The in-scope stream (2.2.x) ships h2 >= 0.4.8 across all versions and is not affected by CVE-2026-48901. However, the 2.1.x stream ships h2 0.4.5 which is below the enriched fix threshold of 0.4.8 from Step 1.5.
