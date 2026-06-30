# Version Impact Analysis — TC-8002

## CVE-2026-28940: serde_json < 1.0.135

### Fix Threshold

- Source: Jira description (external API enrichment not performed in eval mode)
- Fixed version: **1.0.135**
- Affected range: versions before 1.0.135

### Version Impact Table

All supported versions across both streams are analyzed (even though TC-8002 is scoped
to stream 2.2.x, all streams are checked for cross-stream impact awareness).

| Stream | Version | Tag | serde_json version | Affected? | Notes |
|--------|---------|-----|--------------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 1.0.137 | **NO** | >= 1.0.135 |
| 2.1.x | 2.1.1 | v0.3.12 | 1.0.137 | **NO** | >= 1.0.135 |
| 2.2.x | 2.2.0 | v0.4.5 | 1.0.138 | **NO** | >= 1.0.135 |
| 2.2.x | 2.2.1 | v0.4.8 | 1.0.138 | **NO** | >= 1.0.135 |
| 2.2.x | 2.2.2 | v0.4.9 | — | **NO** | retag of 2.2.1 (same as v0.4.8) |
| 2.2.x | 2.2.3 | v0.4.11 | 1.0.139 | **NO** | >= 1.0.135 |
| 2.2.x | 2.2.4 | v0.4.12 | 1.0.139 | **NO** | >= 1.0.135 |

### Summary

**No supported versions are affected.** Every version across all streams ships
serde_json >= 1.0.135, which is at or above the fix threshold.

- Stream 2.1.x: all versions ship serde_json 1.0.137 (not affected)
- Stream 2.2.x: all versions ship serde_json 1.0.138 or 1.0.139 (not affected)

The lowest serde_json version found across all streams is **1.0.137** (in 2.1.x),
which is already above the fix threshold of 1.0.135.

### Dependency Chain Context

Not applicable — no versions are affected, so dependency chain tracing is unnecessary.

### Upstream Fix Check

Not applicable — no versions are affected, so upstream fix status is moot.
