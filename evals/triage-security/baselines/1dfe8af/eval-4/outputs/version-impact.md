# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-33501 (h2 < 0.4.8)

| Version | Stream | Build Tag | h2 Version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (fixed) |
| 2.2.1 | 2.2.x | v0.4.8 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (fixed) |
| 2.2.2 | 2.2.x | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.4.9 | NO | 0.4.9 >= 0.4.8 (fixed) |
| 2.2.4 | 2.2.x | v0.4.12 | 0.4.9 | NO | 0.4.9 >= 0.4.8 (fixed) |

## Stream Impact Summary

| Stream | Affected? | Details |
|--------|-----------|---------|
| 2.1.x | YES | All versions (2.1.0, 2.1.1) ship h2 0.4.5, which is vulnerable |
| 2.2.x | NO | All versions ship h2 >= 0.4.8, which includes the fix |

## Dependency Chain Context

The h2 crate is a Cargo (Rust) dependency in the backend repository. Based on lock file analysis:

- **2.1.x stream**: h2 0.4.5 is shipped in both 2.1.0 (tag v0.3.8) and 2.1.1 (tag v0.3.12). This version is within the affected range (< 0.4.8) and is vulnerable to memory exhaustion via CONTINUATION frames.
- **2.2.x stream**: h2 0.4.8 is shipped starting from 2.2.0 (tag v0.4.5), which is the exact fixed version. Later versions ship 0.4.8 or 0.4.9, all of which are at or above the fix threshold.

The vulnerability allows a peer to send excessive CONTINUATION frames following a HEADERS frame, causing unbounded memory allocation. The fix in 0.4.8 adds a configurable maximum header list size defaulting to 16 KiB.

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | Upstream fix needs to be checked -- h2 must be bumped to >= 0.4.8 on this branch |
| 2.2.x | Cargo | release/0.4.z | Already ships fixed version (h2 >= 0.4.8) -- no action needed |
