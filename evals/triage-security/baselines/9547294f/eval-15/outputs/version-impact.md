# Step 2 -- Version Impact Analysis

## Supportability Matrix (2.2.x Stream)

Source: security-matrix.md for rhtpa-release.0.4.z (2.2.x stream)

| Version | Build | Build Date | backend (pinned tag) | Notes |
|---------|-------|------------|----------------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 | |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 | |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 | |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 | |

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Pinned Tag | quinn-proto | Affected? | Notes |
|---------|------------|-------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |

Each version's dependency version was extracted from the lock file at the pinned commit
tag from the supportability matrix -- not from branch HEAD.

Version 2.2.2 is a retag of 2.2.1 (identical backend source commit v0.4.8), so the
lock file check was skipped and the result carried forward from 2.2.1.

## Cross-Stream Impact (2.1.x Stream)

Although this issue is scoped to the 2.2.x stream, the version impact analysis also
covers the 2.1.x stream for cross-stream awareness:

| Version | Pinned Tag | quinn-proto | Affected? | Notes |
|---------|------------|-------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | 0.11.9 < 0.11.14 |

Both 2.1.x versions ship the vulnerable dependency. This is noted for Step 8 Case B
cross-stream impact analysis.

## Dependency Chain Context

Dependency chain for quinn-proto (Cargo):

- Ecosystem: Cargo (source dependency)
- quinn-proto is a Rust crate used as part of the QUIC protocol stack
- Profile: production (runtime dependency)
- Present in all versions across both streams

## Summary

- **Affected versions (2.2.x)**: 2.2.0, 2.2.1, 2.2.2
- **Not affected versions (2.2.x)**: 2.2.3, 2.2.4
- **Cross-stream**: 2.1.x versions (2.1.0, 2.1.1) are also affected
