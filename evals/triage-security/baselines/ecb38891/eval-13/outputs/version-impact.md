# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

The issue is scoped to stream **2.2.x** (suffix `[rhtpa-2.2]`). All versions in the 2.2.x stream are checked. Cross-stream versions (2.1.x) are also analyzed for Case A cross-stream impact detection.

### 2.2.x Stream (in-scope)

| Version | Tag | quinn-proto | Affected? | Notes |
|---------|-----|-------------|-----------|-------|
| 2.2.0 | `v0.4.5` | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.1 | `v0.4.8` | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.2 | `v0.4.9` | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | `v0.4.11` | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4 | `v0.4.12` | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |

### 2.1.x Stream (cross-stream check)

| Version | Tag | quinn-proto | Affected? | Notes |
|---------|-----|-------------|-----------|-------|
| 2.1.0 | `v0.3.8` | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.1.1 | `v0.3.12` | 0.11.9 | YES | 0.11.9 < 0.11.14 |

### Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency
  Profile: production (quinn-proto is a runtime dependency)

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml
```

### Summary

- **In-scope (2.2.x)**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 ship the fixed version.
- **Cross-stream (2.1.x)**: All versions (2.1.0, 2.1.1) are affected. This will be reported as cross-stream impact in Step 8 Case A.
