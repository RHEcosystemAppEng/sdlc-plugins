# Step 2 — Version Impact Analysis

## Step 0.3 — Matrix Staleness Check

The security-matrix.md has `Last-Updated: 2026-06-28T10:00:00Z`. This is within the 14-day threshold. Staleness check passes silently — no warning presented.

## Supportability Matrix (2.2.x stream — scoped)

The issue is scoped to `[rhtpa-2.2]`, so only the 2.2.x stream versions are analyzed.

| Version | Build | Build Date | backend tag | quinn-proto version | Affected? | Notes |
|---------|-------|------------|-------------|---------------------|-----------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | 0.11.12 | **YES** | 0.11.12 < 0.11.14 |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | — | **YES** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | 0.11.14 | **NO** | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | 0.11.14 | **NO** | 0.11.14 >= 0.11.14 (fixed) |

## Cross-Stream Analysis (Important Rule 4)

Although triage is scoped to 2.2.x, the version impact table includes all versions from the supportability matrix per Important Rule 4. The 2.1.x stream is also checked for cross-stream awareness:

| Version | Build | Build Date | backend tag | quinn-proto version | Affected? | Notes |
|---------|-------|------------|-------------|---------------------|-----------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for quinn-proto:
  backend (workspace) → quinn-proto
  Type: direct dependency
  Profile: production (quinn-proto is a runtime dependency)
  Ecosystem: Cargo

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml
```

## Summary

- **2.2.x stream**: 3 versions affected (2.2.0, 2.2.1, 2.2.2), 2 versions not affected (2.2.3, 2.2.4)
- **2.1.x stream**: 2 versions affected (2.1.0, 2.1.1) — cross-stream impact detected
