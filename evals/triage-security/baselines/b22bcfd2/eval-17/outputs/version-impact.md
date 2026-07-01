# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix

The security-matrix.md was loaded for both configured version streams. The matrix `Last-Updated` timestamp is `2026-06-28T10:00:00Z`, which is within the 14-day threshold (3 days old as of 2026-07-01). Step 0.3 staleness check passed silently.

Since the issue is scoped to stream **2.2.x** (suffix `[rhtpa-2.2]`), version impact analysis focuses on the 2.2.x stream. However, per Important Rule 4, ALL versions from ALL streams in the supportability matrix are checked to detect cross-stream impact.

### Stream 1: 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |

### Stream 2: 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.3 -- Dependency Version Extraction

Using pinned commit tags from the supportability matrix (not branch HEAD), the quinn-proto dependency version was extracted from `Cargo.lock` at each tag:

| Tag | quinn-proto version | Source |
|-----|---------------------|--------|
| `v0.3.8` | 0.11.9 | `git show v0.3.8:Cargo.lock` |
| `v0.3.12` | 0.11.9 | `git show v0.3.12:Cargo.lock` |
| `v0.4.5` | 0.11.9 | `git show v0.4.5:Cargo.lock` |
| `v0.4.8` | 0.11.12 | `git show v0.4.8:Cargo.lock` |
| `v0.4.9` | _(retag of v0.4.8)_ | Carried forward from v0.4.8 |
| `v0.4.11` | 0.11.14 | `git show v0.4.11:Cargo.lock` |
| `v0.4.12` | 0.11.14 | `git show v0.4.12:Cargo.lock` |

## 2.4 -- Version Impact Table

CVE-2026-31812 affects quinn-proto versions **< 0.11.14**. Fixed version: **0.11.14**.

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | **YES** | < 0.11.14 |
| 2.1.1 | 2.1.x | 0.11.9 | **YES** | < 0.11.14 |
| 2.2.0 | 2.2.x | 0.11.9 | **YES** | < 0.11.14 |
| 2.2.1 | 2.2.x | 0.11.12 | **YES** | < 0.11.14 |
| 2.2.2 | 2.2.x | 0.11.12 | **YES** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.11.14 | **NO** | >= 0.11.14 (fixed) |
| 2.2.4 | 2.2.x | 0.11.14 | **NO** | >= 0.11.14 (fixed) |

**Summary**: Versions 2.1.0, 2.1.1, 2.2.0, 2.2.1, and 2.2.2 ship vulnerable quinn-proto (< 0.11.14). Versions 2.2.3 and 2.2.4 ship the fixed version (0.11.14).

### Dependency Chain Context (Step 2.3.5)

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) -> reqwest [features: http3] -> h3 -> quinn -> quinn-proto
  Profile: production (reqwest is a runtime dependency)

  First appeared: all checked versions include quinn-proto
  Direct dependency: No (transitive via reqwest -> h3 -> quinn)
```

### Cross-Stream Impact

The version impact table shows that stream **2.1.x** is also affected (versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9). This is outside the current issue's scope (scoped to 2.2.x) and will be handled in Step 8 Case B (cross-stream impact).
