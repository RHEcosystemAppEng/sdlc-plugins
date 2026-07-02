# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-33501 (h2 < 0.4.8)

| Version | Stream | Build Tag | h2 version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | YES | < 0.4.8 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | YES | < 0.4.8 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.4.8 | NO | >= 0.4.8 (fixed) |
| 2.2.1 | 2.2.x | v0.4.8 | 0.4.8 | NO | >= 0.4.8 (fixed) |
| 2.2.2 | 2.2.x | v0.4.9 | -- | NO | retag of 2.2.1 |
| 2.2.3 | 2.2.x | v0.4.11 | 0.4.9 | NO | >= 0.4.8 (fixed) |
| 2.2.4 | 2.2.x | v0.4.12 | 0.4.9 | NO | >= 0.4.8 (fixed) |

## Summary

- **2.1.x stream**: ALL versions affected (2.1.0, 2.1.1) -- h2 0.4.5 is below the fix threshold of 0.4.8
- **2.2.x stream**: NO versions affected -- all versions ship h2 >= 0.4.8 (the fixed version)

## Dependency Chain Context

Dependency chain for h2 (Cargo):
- Ecosystem: Cargo (Rust crate)
- Lock file: `Cargo.lock`
- h2 is a transitive dependency of the backend service (likely via hyper or similar HTTP stack)
- The h2 crate handles HTTP/2 CONTINUATION frame processing

Present in: 2.1.x (h2 0.4.5 -- vulnerable) and 2.2.x (h2 >= 0.4.8 -- fixed)

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | h2 at HEAD | Fixed? |
|--------|-----------|-----------------|------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.4.5 | NO |
| 2.2.x | Cargo | release/0.4.z | 0.4.9 | YES |

The 2.1.x upstream branch (`release/0.3.z`) has NOT been fixed -- h2 remains at 0.4.5. Remediation requires an upstream PR to bump h2 to >= 0.4.8 on `release/0.3.z`, followed by a downstream propagation in the Konflux release repo.

The 2.2.x upstream branch (`release/0.4.z`) already ships h2 0.4.9 (>= 0.4.8) -- no remediation needed.
