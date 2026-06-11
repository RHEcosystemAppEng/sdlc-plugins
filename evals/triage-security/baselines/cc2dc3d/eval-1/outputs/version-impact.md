# Step 2 -- Version Impact Analysis

## Supportability Matrix

Data aggregated from both Konflux release repos (rhtpa-release.0.3.z for 2.1.x stream and rhtpa-release.0.4.z for 2.2.x stream).

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | backend tag |
|---------|-------|------------|-------------|
| 2.1.0 | 0.3.8 | 2025-09-15 | v0.3.8 |
| 2.1.1 | 0.3.12 | 2025-11-20 | v0.3.12 |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Build Date | backend tag |
|---------|-------|------------|-------------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 (retag of 2.2.1) |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 |

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | |
| 2.1.1 | 0.11.9 | YES | |
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 0.11.14 | NO | ships fixed version |

**Summary**: Versions 2.1.0, 2.1.1, 2.2.0, 2.2.1, and 2.2.2 ship vulnerable versions of quinn-proto (< 0.11.14). Versions 2.2.3 and 2.2.4 ship the fixed version (0.11.14) and are NOT affected.

## Dependency Chain Context

Dependency chain for quinn-proto (Cargo ecosystem):

- Ecosystem: Cargo (Rust crate)
- Lock file: Cargo.lock
- The vulnerable package quinn-proto is a dependency in the backend repository
- quinn-proto was present starting from version 2.1.0 (tag v0.3.8, quinn-proto 0.11.9)
- The fix (0.11.14) was picked up in version 2.2.3 (tag v0.4.11)

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fixed at branch? | Notes |
|--------|-----------|-----------------|------------------|-------|
| 2.1.x | Cargo | release/0.3.z | Unknown | Would need to check branch HEAD; last released tag (v0.3.12) ships 0.11.9 (vulnerable) |
| 2.2.x | Cargo | release/0.4.z | YES | Tag v0.4.11 already ships 0.11.14 (fixed); latest tag v0.4.12 also ships 0.11.14 |

The 2.2.x stream has the fix available upstream starting from tag v0.4.11. For the 2.1.x stream, the latest known tag (v0.3.12) still ships the vulnerable version 0.11.9.
