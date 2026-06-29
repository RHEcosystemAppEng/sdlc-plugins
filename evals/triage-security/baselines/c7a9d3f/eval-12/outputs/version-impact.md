# Step 2 -- Version Impact Analysis

## Enriched Fix Threshold

From Step 1.5 cross-validation: **h2 < 0.4.8** are affected (fix threshold: 0.4.8).

This enriched threshold is used for all comparisons below, replacing the imprecise Jira description data ("versions prior to the fix").

## Version Impact Table for CVE-2026-48901 (h2 < 0.4.8)

### Stream 2.2.x (issue scope: rhtpa-2.2)

| Version | Build Tag | h2 version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.4.8 | NO | h2 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.1 | v0.4.8 | 0.4.8 | NO | h2 0.4.8 >= 0.4.8 |
| 2.2.2 | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.4.9 | NO | h2 0.4.9 >= 0.4.8 |
| 2.2.4 | v0.4.12 | 0.4.9 | NO | h2 0.4.9 >= 0.4.8 |

**Result for scoped stream 2.2.x: NO versions affected.** All versions in the 2.2.x stream ship h2 >= 0.4.8 which is at or above the fix threshold.

### Stream 2.1.x (cross-stream analysis, outside issue scope)

| Version | Build Tag | h2 version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.4.5 | YES | h2 0.4.5 < 0.4.8 |
| 2.1.1 | v0.3.12 | 0.4.5 | YES | h2 0.4.5 < 0.4.8 |

**Result for stream 2.1.x: ALL versions affected.** Both versions in the 2.1.x stream ship h2 0.4.5 which is below the fix threshold of 0.4.8.

## Dependency Chain Context (Step 2.3.5)

h2 is a Cargo (Rust) crate -- a source-level dependency in the backend component. The dependency chain for h2 in the backend workspace would typically be:

```
backend (workspace) -> hyper -> h2
```

h2 is a transitive dependency brought in through the HTTP stack. It provides the HTTP/2 protocol implementation used by hyper for HTTP/2 connections.

- **Ecosystem**: Cargo (source dependency)
- **Profile**: production (h2 is a runtime dependency, not dev-only)
- **Present in**: both 2.1.x and 2.2.x streams (all build tags include h2)

## Combined Summary

| Stream | Versions Affected | h2 Versions Shipped | Verdict |
|--------|-------------------|---------------------|---------|
| 2.2.x (scoped) | 0 of 5 | 0.4.8, 0.4.9 | NOT AFFECTED |
| 2.1.x (cross-stream) | 2 of 2 | 0.4.5 | AFFECTED |

## Triage Implication

Since the issue is scoped to stream 2.2.x (suffix `[rhtpa-2.2]`) and NO versions in that stream are affected, this is a **Case C** scenario: close as Not a Bug for the scoped stream.

However, cross-stream analysis reveals that the 2.1.x stream IS affected (all versions ship h2 0.4.5 < 0.4.8). This constitutes a **Case B** cross-stream impact that should be reported.
