# Step 2 -- Version Impact Analysis: TC-8020

## CVE Details

- **CVE**: CVE-2026-55123
- **Library**: tokio
- **Affected range**: versions before 1.42.0
- **Fixed version**: 1.42.0

## Version Impact Table

Version Impact for CVE-2026-55123 (tokio < 1.42.0):

| Version | Stream | tokio version | Affected? | Notes |
|---------|--------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 (2.1.x) | 1.40.0 | **YES** | Source tag: v0.3.8 |
| RHTPA 2.1.1 | rhtpa-2.1 (2.1.x) | 1.40.0 | **YES** | Source tag: v0.3.12 |
| RHTPA 2.2.0 | rhtpa-2.2 (2.2.x) | 1.41.1 | **YES** | Source tag: v0.4.5 |
| RHTPA 2.2.1 | rhtpa-2.2 (2.2.x) | 1.41.1 | **YES** | Source tag: v0.4.8 |

All four versions across both streams ship tokio < 1.42.0 and are affected.

## Cross-Stream Impact Summary

| Stream | Versions affected | tokio version(s) found | In issue scope? |
|--------|-------------------|------------------------|-----------------|
| rhtpa-2.2 (2.2.x) | RHTPA 2.2.0, RHTPA 2.2.1 | 1.41.1 | **YES** (issue suffix `[rhtpa-2.2]`) |
| rhtpa-2.1 (2.1.x) | RHTPA 2.1.0, RHTPA 2.1.1 | 1.40.0 | **NO** (different stream) |

Stream rhtpa-2.1 is **outside** the scope of TC-8020 but is also affected. This triggers Case B (cross-stream impact / proactive remediation) in Step 7.

## Dependency Chain Context

```
Dependency chain for tokio:
  backend (workspace) -> tokio (Cargo dependency)
  Ecosystem: Cargo
  Lock file: Cargo.lock
  Profile: production (tokio is a runtime dependency for async Rust)
```

tokio is a direct or near-direct runtime dependency in the backend workspace. As a fundamental async runtime crate, it is a core production dependency -- not dev-only or feature-gated.

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix threshold | Status |
|--------|-----------|-----------------|---------------|--------|
| 2.2.x | Cargo | release/0.4.z | 1.42.0 | Needs upstream backport or dependency bump |
| 2.1.x | Cargo | release/0.3.z | 1.42.0 | Needs upstream backport or dependency bump |

Upstream fix PR: [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001)
