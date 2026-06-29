# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Aggregated Supportability Matrix

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

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | 2.1.x | 0.11.9 | YES | < 0.11.14 |
| 2.2.0 | 2.2.x | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 2.2.x | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | 2.2.x | 0.11.14 | NO | >= 0.11.14 (fixed) |

## Dependency Chain Context

Dependency chain for quinn-proto (Cargo):
- Ecosystem: Cargo (Rust crate)
- Lock file: `Cargo.lock`
- quinn-proto is a QUIC protocol implementation crate from the quinn-rs project
- The vulnerability allows a remote attacker to cause a panic via excessive stream counts in QUIC transport frames (DoS)

The fix was introduced in quinn-proto 0.11.14. Versions 2.2.3 (tag v0.4.11) and 2.2.4 (tag v0.4.12) already ship the fixed version.

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | (needs verification) | Unknown -- lock file data shows v0.3.12 ships 0.11.9 |
| 2.2.x | Cargo | release/0.4.z | (needs verification) | Likely YES -- v0.4.11+ ships 0.11.14 |

Note: In a real triage, `git show release/0.4.z:Cargo.lock` and `git show release/0.3.z:Cargo.lock` would be run at branch HEAD to verify the upstream fix status. Based on the mock data, the latest released tags on each stream show:
- 2.1.x: latest tag v0.3.12 still ships quinn-proto 0.11.9 (NOT fixed)
- 2.2.x: latest tag v0.4.12 ships quinn-proto 0.11.14 (fixed as of v0.4.11)

## Summary

- **2.1.x stream**: ALL versions affected (2.1.0, 2.1.1) -- ships quinn-proto 0.11.9
- **2.2.x stream**: versions 2.2.0, 2.2.1, 2.2.2 are affected; versions 2.2.3, 2.2.4 are NOT affected (already fixed)
- The fix was picked up in the 2.2.x stream starting at build v0.4.11 (version 2.2.3, released 2026-03-23)
- The 2.1.x stream has NOT picked up the fix in any released version
