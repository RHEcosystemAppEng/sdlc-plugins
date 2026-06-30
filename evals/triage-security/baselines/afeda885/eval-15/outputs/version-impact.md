# Step 2 — Version Impact Analysis for CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | — | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | fixed at 0.11.14 |
| 2.2.4 | 2.2.x | 0.11.14 | NO | fixed at 0.11.14 |

## Dependency Chain Context

Dependency chain for quinn-proto (Cargo):
- Ecosystem: Cargo (Rust crate)
- Lock file: `Cargo.lock` in the backend repository
- Source pinning: `artifacts.lock.yaml` (download URL contains tag)

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Lock File | Notes |
|--------|-----------|-----------------|-----------|-------|
| 2.1.x | Cargo | release/0.3.z | Cargo.lock | Latest tag v0.3.12 ships 0.11.9 — NOT fixed upstream |
| 2.2.x | Cargo | release/0.4.z | Cargo.lock | Tags v0.4.11+ ship 0.11.14 — fixed upstream since 2.2.3 |

## Cross-Stream Summary

- **Stream 2.2.x (issue scope)**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship the fix (quinn-proto 0.11.14).
- **Stream 2.1.x (cross-stream)**: All versions (2.1.0, 2.1.1) are affected — they ship quinn-proto 0.11.9, which is below the fix threshold of 0.11.14.
