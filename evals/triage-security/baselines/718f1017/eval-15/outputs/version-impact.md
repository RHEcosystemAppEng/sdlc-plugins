# Step 2 -- Version Impact Analysis for CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | fixed: ships >= 0.11.14 |
| 2.2.4 | 2.2.x | 0.11.14 | NO | fixed: ships >= 0.11.14 |

## Dependency Chain Context

Dependency chain for quinn-proto (Cargo):
- Ecosystem: Cargo (Rust crate)
- Lock file: Cargo.lock
- Repository: backend (rhtpa-backend)
- Profile: production dependency

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | YES |

Upstream fix is available -- remediation is a Konflux release repo change to bump the source tag/commit reference.

## Cross-Stream Impact

Stream 2.1.x is also affected (versions 2.1.0 and 2.1.1 ship quinn-proto 0.11.9). This issue is scoped to stream 2.2.x, so 2.1.x impact will be reported as cross-stream impact in Step 7 (Case B).
