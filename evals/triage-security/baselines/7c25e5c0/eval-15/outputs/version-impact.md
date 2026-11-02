# Step 2 — Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

All versions from the supportability matrix are included — no versions skipped (Important Rule 4).

### 2.2.x Stream (scoped — primary analysis)

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.2 | v0.4.9 | — | YES | retag of 2.2.1 — same as 2.2.1 (0.11.12) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (at fix threshold) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (at fix threshold) |

### 2.1.x Stream (cross-stream check)

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | 0.11.9 < 0.11.14 |

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for quinn-proto:
  backend (workspace) → quinn-proto
  Type: direct dependency
  Profile: production (quinn-proto is a runtime dependency)

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml
```

## Summary

- **2.2.x stream**: 3 affected versions (2.2.0, 2.2.1, 2.2.2), 2 not affected (2.2.3, 2.2.4)
- **2.1.x stream**: All 2 versions affected (2.1.0, 2.1.1) — cross-stream impact detected
