# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-33501 (h2 < 0.4.8)

| Version | Stream | Source Tag | h2 Version | Affected? | Notes |
|---------|--------|------------|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | YES | < 0.4.8 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | YES | < 0.4.8 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.4.8 | NO | >= 0.4.8 (fixed) |
| 2.2.1 | 2.2.x | v0.4.8 | 0.4.8 | NO | >= 0.4.8 (fixed) |
| 2.2.2 | 2.2.x | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.4.9 | NO | >= 0.4.8 (fixed) |
| 2.2.4 | 2.2.x | v0.4.12 | 0.4.9 | NO | >= 0.4.8 (fixed) |

## Stream Impact Summary

| Stream | Affected? | Affected Versions | Details |
|--------|-----------|-------------------|---------|
| 2.1.x | YES | 2.1.0, 2.1.1 | All versions ship h2 0.4.5 (< 0.4.8) |
| 2.2.x | NO | (none) | All versions ship h2 >= 0.4.8 |

## Dependency Chain Context

Dependency chain for h2 (Cargo):
- Ecosystem: Cargo (Rust crate)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`

The h2 crate is present in all versions across both streams. In the 2.1.x stream, h2 0.4.5 is shipped, which is within the affected range (< 0.4.8). In the 2.2.x stream, h2 was updated to 0.4.8+ starting from version 2.2.0, which is at or above the fix threshold.

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | Requires upstream backport -- h2 must be bumped to >= 0.4.8 |
| 2.2.x | Cargo | release/0.4.z | Already fixed -- h2 >= 0.4.8 in all versions |
