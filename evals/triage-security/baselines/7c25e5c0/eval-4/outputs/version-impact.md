# Step 2 — Version Impact Analysis

## Version Impact for CVE-2026-33501 (h2 < 0.4.8)

The issue is **unscoped** — all versions across all streams are checked.

| Version | Stream | Source Pin | h2 version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.4.8 | **NO** | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.4.8 | **NO** | 0.4.8 >= 0.4.8 |
| 2.2.2 | 2.2.x | `v0.4.9` | — | **NO** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.4.9 | **NO** | 0.4.9 >= 0.4.8 |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.4.9 | **NO** | 0.4.9 >= 0.4.8 |

## Summary

- **2.1.x stream**: ALL versions affected (2.1.0, 2.1.1) — ship h2 0.4.5
- **2.2.x stream**: NO versions affected — all versions ship h2 >= 0.4.8 (the fix threshold)

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for h2:
  backend (workspace) → h2
  Type: direct dependency (present in Cargo.lock as a direct dependency)
  Profile: production (h2 is a runtime HTTP/2 implementation dependency)

Remediation: bump h2 to >= 0.4.8 in Cargo.toml on release/0.3.z branch
```

Only the 2.1.x stream requires remediation. The 2.2.x stream already ships h2 0.4.8+.
