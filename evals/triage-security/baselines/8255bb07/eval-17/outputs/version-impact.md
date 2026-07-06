# Step 2 -- Version Impact Analysis

## Supportability Matrix Sources

Data loaded from two version streams configured in Security Configuration:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

## Ecosystem Mappings

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | Cargo.lock | `git show <tag>:Cargo.lock` | release/0.3.z (2.1.x), release/0.4.z (2.2.x) |

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Build Tag | quinn-proto | Affected? | Notes |
|--------|---------|-----------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | **YES** | |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | **YES** | |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | **YES** | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | **YES** | |
| 2.2.x | 2.2.2 | v0.4.9 | -- | **YES** | retag of 2.2.1 (same as v0.4.8) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | fixed version (>= 0.11.14) |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | fixed version (>= 0.11.14) |

## Analysis Summary

### Issue stream (2.2.x)

- Versions 2.2.0, 2.2.1, and 2.2.2 ship quinn-proto < 0.11.14 and are **affected**.
- Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (the fixed version) and are **not affected**.
- The fix was already picked up in the 2.2.x stream starting from build 0.4.11 (version 2.2.3). The latest release in this stream already includes the fix.

### Cross-stream impact (2.1.x)

- All versions in the 2.1.x stream (2.1.0, 2.1.1) ship quinn-proto 0.11.9, which is within the affected range (< 0.11.14). The 2.1.x stream is **fully affected**.
- This is outside the issue's stream scope ([rhtpa-2.2]) and will be handled as Case B (cross-stream impact) in Step 8.

## Dependency Chain Context

```
Dependency chain for quinn-proto (Cargo):
  Ecosystem: Cargo (Rust crate)
  Lock file: Cargo.lock
  Source repository: rhtpa-backend

  quinn-proto is a QUIC transport protocol implementation crate.
  The vulnerability allows a remote attacker to cause a panic via
  excessive stream counts in QUIC transport frames (DoS).

  Versions affected: 0.11.9, 0.11.12 (all < 0.11.14)
  Fix threshold: 0.11.14
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix Status |
|--------|-----------|-----------------|------------|
| 2.1.x | Cargo | release/0.3.z | Needs upstream backport |
| 2.2.x | Cargo | release/0.4.z | Already fixed (v0.4.11+) |

Upstream fix PR: [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048)

## Affects Versions Correction (Step 3 Preview)

Current Affects Versions: `RHTPA 2.0.0` (incorrect -- no 2.0.x stream exists)

Proposed correction for the scoped stream (2.2.x):
- **Remove**: RHTPA 2.0.0
- **Add**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

Versions 2.2.3 and 2.2.4 are not affected and should not be in Affects Versions.
