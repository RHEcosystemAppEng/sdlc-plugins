# Step 2 -- Version Impact Analysis for CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Pinned Commit Tag | quinn-proto | Affected? | Notes |
|---------|--------|-------------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | YES | < 0.11.14 |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | YES | retag of 2.2.1 (same as 2.2.1: backend pinned commit v0.4.8) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | >= 0.11.14 (fixed) |

**Key observations:**
- ALL versions from BOTH streams in the supportability matrix are included (Important Rule 4).
- Dependency versions are extracted using the **pinned commit tags** from the supportability matrix, not branch HEAD (Important Rule 13).
- Version 2.2.2 is identified as a **retag of 2.2.1** (same backend commit `v0.4.8`). Its affected status is carried forward from 2.2.1 without re-running the lock file check (Important Rule 5).
- Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14, which is the fixed version and therefore NOT affected.

## Dependency Chain Context

Dependency chain for quinn-proto (Cargo):

The lock file inspection at each pinned commit shows quinn-proto is present in the Cargo.lock, confirming it is a source-level dependency of the backend workspace.

- Profile: production (runtime dependency)
- Present in all versions across both streams (2.1.x and 2.2.x)

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Notes |
|--------|-----------|-----------------|-------|
| 2.2.x | Cargo | release/0.4.z | Upstream fix available: quinn-rs/quinn#2048 |
| 2.1.x | Cargo | release/0.3.z | Upstream fix available: quinn-rs/quinn#2048 |

The upstream fix PR (quinn-rs/quinn#2048) patches quinn-proto to version 0.11.14. Versions 2.2.3+ already incorporate this fix; remediation is needed for 2.2.0, 2.2.1, and 2.2.2 (within the scoped 2.2.x stream), and for 2.1.0 and 2.1.1 (in the 2.1.x stream, which is outside this issue's scope).
