# Step 2 -- Version Impact Analysis

## Fix Threshold Source

The fix threshold used for version impact comparison is **0.4.8**, obtained from Step 1.5 External CVE Data Enrichment (cross-validated between MITRE CVE API and OSV.dev). The Jira description data was imprecise ("versions prior to the fix" / "see advisory") and is NOT used for these comparisons.

## Version Impact Table

Version Impact for CVE-2026-48901 (h2 < 0.4.8):

| Version | h2 version | Affected? | Notes |
|---------|-----------|-----------|-------|
| 2.2.0 | 0.4.5 | YES | h2 0.4.5 < 0.4.8 (enriched threshold from Step 1.5) |
| 2.2.1 | 0.4.8 | NO | h2 0.4.8 >= 0.4.8 |
| 2.2.2 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.4.9 | NO | h2 0.4.9 >= 0.4.8 |
| 2.2.4 | 0.4.9 | NO | h2 0.4.9 >= 0.4.8 |

**Note**: Version comparisons use the enriched fix threshold (0.4.8) from Step 1.5, not the imprecise Jira description data.

## Evidence

- **2.2.0** (tag `v0.4.5`): `git show v0.4.5:Cargo.lock` shows h2 = 0.4.5. This is less than the enriched fix threshold 0.4.8. **AFFECTED**.
- **2.2.1** (tag `v0.4.8`): `git show v0.4.8:Cargo.lock` shows h2 = 0.4.8. This equals the fix threshold 0.4.8 (i.e., >= 0.4.8). **NOT AFFECTED**.
- **2.2.2** (tag `v0.4.9`): This is a retag of 2.2.1 (backend tag `v0.4.8` is the same). Result carried forward from 2.2.1. **NOT AFFECTED**.
- **2.2.3** (tag `v0.4.11`): `git show v0.4.11:Cargo.lock` shows h2 = 0.4.9. This exceeds the fix threshold 0.4.8. **NOT AFFECTED**.
- **2.2.4** (tag `v0.4.12`): `git show v0.4.12:Cargo.lock` shows h2 = 0.4.9. This exceeds the fix threshold 0.4.8. **NOT AFFECTED**.

## Dependency Chain Context

```
Dependency chain for h2 (Cargo):
  h2 is a Rust crate providing HTTP/2 protocol support.
  Profile: production (h2 is a runtime dependency used for HTTP/2 connections)
  
  Present in: 2.2.0 (v0.4.5) at version 0.4.5 — AFFECTED
  Fixed from: 2.2.1 (v0.4.8) onwards at version 0.4.8+
```

## Summary

Only version **2.2.0** is affected within the 2.2.x stream. Versions 2.2.1 through 2.2.4 ship h2 >= 0.4.8 and are not affected.
