# Version Impact — TC-8004

## Version Impact Table

Version Impact for CVE-2026-33501 (h2 < 0.4.8):

| Version | Stream | h2 version | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0   | 2.1.x  | 0.4.5      | YES       | Source tag v0.3.8 |
| 2.1.1   | 2.1.x  | 0.4.5      | YES       | Source tag v0.3.12 |
| 2.2.0   | 2.2.x  | 0.4.8      | NO        | Source tag v0.4.5; ships fix version |
| 2.2.1   | 2.2.x  | 0.4.8      | NO        | Source tag v0.4.8 |
| 2.2.2   | 2.2.x  | 0.4.8      | NO        | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3   | 2.2.x  | 0.4.9      | NO        | Source tag v0.4.11 |
| 2.2.4   | 2.2.x  | 0.4.9      | NO        | Source tag v0.4.12 |

## Impact Summary

- **Stream 2.1.x**: AFFECTED — all versions (2.1.0, 2.1.1) ship h2 0.4.5, which is below the fix threshold of 0.4.8.
- **Stream 2.2.x**: NOT AFFECTED — all versions ship h2 >= 0.4.8 (the fix version or later).

## Dependency Chain Context

Dependency chain for h2 (Cargo):
- Ecosystem: Cargo (Rust crate)
- Lock file: Cargo.lock
- The h2 crate provides HTTP/2 protocol support. It is a transitive dependency typically pulled in via hyper/reqwest or similar HTTP client/server libraries.
- Stream 2.1.x ships h2 0.4.5 across all releases (v0.3.8 and v0.3.12 source tags).
- Stream 2.2.x ships h2 0.4.8+ starting from the earliest release (v0.4.5 source tag), meaning the fix was already present when stream 2.2.x began shipping.

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Notes |
|--------|-----------|-----------------|-------|
| 2.1.x  | Cargo     | release/0.3.z   | Remediation needed — h2 must be bumped to >= 0.4.8 |
| 2.2.x  | Cargo     | release/0.4.z   | Already fixed — h2 >= 0.4.8 in all versions |
