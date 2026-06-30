# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Supportability Matrix

Two version streams loaded from security-matrix.md files:

- **Stream 2.1.x** (rhtpa-release.0.3.z): versions 2.1.0, 2.1.1
- **Stream 2.2.x** (rhtpa-release.0.4.z): versions 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4

## Version Impact Table

CVE-2026-31812 affects quinn-proto versions before 0.11.14 (fix threshold: >= 0.11.14).

| Version | Stream | Source Tag | quinn-proto | Affected? | Notes |
|---------|--------|------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | backend retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Dependency Chain Context (Step 2.3.5)

Ecosystem: Cargo (source-level dependency).
quinn-proto is a Rust crate dependency in the backend workspace. The dependency chain is:

```
backend (workspace) -> quinn -> quinn-proto
```

Profile: production (quinn is a runtime networking dependency).

quinn-proto is present in all versions across both streams (2.1.x and 2.2.x). The version was bumped from 0.11.9 to 0.11.12 in v0.4.8, and then to the fixed version 0.11.14 in v0.4.11.

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Fixed Upstream? | Notes |
|--------|-----------|-----------------|-----------------|-------|
| 2.1.x | Cargo | release/0.3.z | To be verified | Requires `git show release/0.3.z:Cargo.lock` |
| 2.2.x | Cargo | release/0.4.z | YES (inferred) | v0.4.11+ ships 0.11.14 |

Note: Versions 2.2.3 (v0.4.11) and 2.2.4 (v0.4.12) already ship quinn-proto 0.11.14, confirming the fix was picked up on the release/0.4.z branch by those releases.

## Cross-Stream Impact Summary

- **Stream 2.2.x** (issue scope): versions 2.2.0, 2.2.1, 2.2.2 are AFFECTED; versions 2.2.3, 2.2.4 are NOT affected.
- **Stream 2.1.x** (out of scope for this issue): versions 2.1.0, 2.1.1 are AFFECTED. This is cross-stream impact -- will be reported via Case B in Step 7.
