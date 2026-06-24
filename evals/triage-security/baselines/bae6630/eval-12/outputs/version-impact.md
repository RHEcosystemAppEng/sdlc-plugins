# Step 2 -- Version Impact Analysis

## Fix Threshold

Using the **enriched fix threshold** from Step 1.5: **< 0.4.8** (affected), **>= 0.4.8** (fixed).

This threshold was cross-validated from MITRE CVE API (`lessThan: 0.4.8`) and OSV.dev (`fixed: 0.4.8`). Both external sources agree. The Jira description's imprecise "versions prior to the fix" is superseded by this structured data.

## Ecosystem

**Cargo** -- the vulnerable library `h2` is a Rust crate. Lock file: `Cargo.lock`. Check command: `git show <tag>:Cargo.lock`.

## Version Impact Table

Version impact for CVE-2026-48901 (h2 < 0.4.8):

### Stream 2.2.x (issue scope: [rhtpa-2.2])

| Version | Build | Backend Tag | h2 version | Affected? | Notes |
|---------|-------|-------------|------------|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 0.4.8 | NO | ships fixed version |
| 2.2.1 | 0.4.8 | `v0.4.8` | 0.4.8 | NO | ships fixed version |
| 2.2.2 | 0.4.9 | `v0.4.8` | 0.4.8 | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.4.11 | `v0.4.11` | 0.4.9 | NO | ships fixed version |
| 2.2.4 | 0.4.12 | `v0.4.12` | 0.4.9 | NO | ships fixed version |

**Result for 2.2.x stream: NO versions affected.** All versions in the 2.2.x stream ship h2 >= 0.4.8, which is at or above the fix threshold.

### Stream 2.1.x (cross-stream analysis)

| Version | Build | Backend Tag | h2 version | Affected? | Notes |
|---------|-------|-------------|------------|-----------|-------|
| 2.1.0 | 0.3.8 | `v0.3.8` | 0.4.5 | YES | below fix threshold (0.4.5 < 0.4.8) |
| 2.1.1 | 0.3.12 | `v0.3.12` | 0.4.5 | YES | below fix threshold (0.4.5 < 0.4.8) |

**Result for 2.1.x stream: ALL versions affected.** Both versions in the 2.1.x stream ship h2 0.4.5, which is below the fix threshold of 0.4.8.

## Dependency Chain Context

h2 is a Cargo (Rust) source dependency. The dependency chain in the backend service is:

```
backend (workspace) -> hyper -> h2 (vulnerable library)
```

h2 provides the HTTP/2 protocol implementation used by the hyper HTTP library. It is a production dependency (not dev-only or build-only), meaning the vulnerable code is present in shipped binaries.

## Summary

- **Issue-scoped stream (2.2.x)**: No versions affected -- all ship h2 >= 0.4.8
- **Cross-stream (2.1.x)**: All versions affected -- both ship h2 0.4.5 (< 0.4.8)

The enriched fix threshold from Step 1.5 (0.4.8) was essential for this analysis. Without external CVE data enrichment, the imprecise Jira description ("versions prior to the fix") would not have provided a usable version constraint for comparison.
