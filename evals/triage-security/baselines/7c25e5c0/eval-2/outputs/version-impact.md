# Step 2 — Version Impact Analysis

## Version Impact for CVE-2026-28940 (serde_json < 1.0.135)

The issue is scoped to the **2.2.x** stream per the `[rhtpa-2.2]` suffix. All versions in the 2.2.x supportability matrix are checked.

| Version | Build | Pinned Commit | serde_json Version | Affected? | Notes |
|---------|-------|---------------|-------------------|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 1.0.138 | **NO** | 1.0.138 >= 1.0.135 (fix threshold) |
| 2.2.1 | 0.4.8 | `v0.4.8` | 1.0.138 | **NO** | 1.0.138 >= 1.0.135 (fix threshold) |
| 2.2.2 | 0.4.9 | `v0.4.8` | 1.0.138 | **NO** | retag of 2.2.1 — same as 2.2.1 |
| 2.2.3 | 0.4.11 | `v0.4.11` | 1.0.139 | **NO** | 1.0.139 >= 1.0.135 (fix threshold) |
| 2.2.4 | 0.4.12 | `v0.4.12` | 1.0.139 | **NO** | 1.0.139 >= 1.0.135 (fix threshold) |

## Summary

**All supported versions in the 2.2.x stream ship serde_json >= 1.0.135**, which is outside the CVE's affected range (< 1.0.135). No supported version is affected.

- Lowest serde_json version across all 2.2.x builds: **1.0.138** (versions 2.2.0, 2.2.1, 2.2.2)
- Fix threshold: **1.0.135**
- All versions are patched: 1.0.138 > 1.0.135

## Dependency Chain Context

```
Dependency chain for serde_json:
  backend (workspace) → serde_json
  Type: direct dependency
  Profile: production (serde_json is a runtime dependency for JSON serialization)
```

No remediation needed — the dependency is already at a safe version across all supported builds.
