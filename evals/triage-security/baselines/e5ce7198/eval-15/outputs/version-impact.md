# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | out-of-scope stream |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | out-of-scope stream |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Dependency Chain Context

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) -> quinn -> quinn-proto
  Ecosystem: Cargo (Rust crate)
  Lock file: Cargo.lock
  Profile: production (quinn is a runtime dependency)

  First affected: 2.1.0 (v0.3.8, quinn-proto 0.11.9)
  Fixed from: 2.2.3 (v0.4.11, quinn-proto 0.11.14)
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Repository | Notes |
|--------|-----------|-----------------|------------|-------|
| 2.2.x | Cargo | release/0.4.z | backend | v0.4.11+ already ships 0.11.14 (fixed) |
| 2.1.x | Cargo | release/0.3.z | backend | v0.3.12 ships 0.11.9 (still affected) |

## Cross-Stream Impact

The 2.1.x stream is **also affected** (versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9). However, this issue is scoped to stream 2.2.x only. The 2.1.x impact will be reported via cross-stream notice (Step 7, Case B).

## Summary

- **Scoped stream (2.2.x)**: 3 versions affected (2.2.0, 2.2.1, 2.2.2), 2 versions already fixed (2.2.3, 2.2.4)
- **Out-of-scope stream (2.1.x)**: 2 versions affected (2.1.0, 2.1.1) -- reported via cross-stream impact
- Remediation needed for the 2.2.x stream (upstream backport + downstream propagation)
