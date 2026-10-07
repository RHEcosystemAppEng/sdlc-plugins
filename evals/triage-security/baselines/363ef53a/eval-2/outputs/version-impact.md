# Version Impact Analysis -- CVE-2026-28940

## Supportability Matrix Source

- Stream 2.1.x: loaded from security-matrix.md (Last-Updated: 2026-06-28T10:00:00Z -- 101 days ago, stale but proceeding per eval constraints)
- Stream 2.2.x: loaded from security-matrix.md (Last-Updated: 2026-06-28T10:00:00Z -- 101 days ago, stale but proceeding per eval constraints)

## Version Impact Table

CVE-2026-28940 affects serde_json versions **before 1.0.135** (fix threshold: >= 1.0.135).

### Stream 2.1.x (out of scope -- included for cross-stream analysis)

| Version | Source Tag | serde_json Version | Affected? | Notes |
|---------|------------|--------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 1.0.137 | **NO** | Ships fixed version (1.0.137 >= 1.0.135) |
| 2.1.1 | v0.3.12 | 1.0.137 | **NO** | Ships fixed version (1.0.137 >= 1.0.135) |

### Stream 2.2.x (in scope -- issue scoped to this stream)

| Version | Source Tag | serde_json Version | Affected? | Notes |
|---------|------------|--------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 1.0.138 | **NO** | Ships fixed version (1.0.138 >= 1.0.135) |
| 2.2.1 | v0.4.8 | 1.0.138 | **NO** | Ships fixed version (1.0.138 >= 1.0.135) |
| 2.2.2 | v0.4.9 | -- | **NO** | Retag of 2.2.1 (same as v0.4.8: 1.0.138) |
| 2.2.3 | v0.4.11 | 1.0.139 | **NO** | Ships fixed version (1.0.139 >= 1.0.135) |
| 2.2.4 | v0.4.12 | 1.0.139 | **NO** | Ships fixed version (1.0.139 >= 1.0.135) |

## Summary

**No supported versions are affected.** Every version across both streams ships serde_json >= 1.0.137, which is above the fix threshold of 1.0.135. The vulnerability was already remediated before these versions were built.

- 2.1.x stream: all versions ship 1.0.137 -- NOT affected
- 2.2.x stream: all versions ship 1.0.138 or 1.0.139 -- NOT affected
- Oldest shipped version (1.0.137 in 2.1.0) is still above the fix threshold (1.0.135)
