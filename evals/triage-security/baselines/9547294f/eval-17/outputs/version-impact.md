# Step 2 -- Version Impact Analysis

## Step 0.3 -- Matrix Staleness Check

The security-matrix.md has `Last-Updated: 2026-06-28T10:00:00Z`, which is 3 days ago (within the 14-day threshold). Proceeding without staleness warning.

## Supportability Matrix

Loaded from security-matrix.md. The issue is scoped to stream **2.2.x** (suffix `[rhtpa-2.2]`), but per Important Rule 4, ALL versions from ALL streams in the supportability matrix are checked.

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | v0.3.8 | |
| 2.1.1 | 0.3.12 | 2025-11-20 | v0.3.12 | |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 | |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 | |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 | |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 | |

## Ecosystem

Cargo (Rust) -- lock file: `Cargo.lock`, check command: `git show <tag>:Cargo.lock`

## Dependency Version Extraction

Using pinned commit tags from the supportability matrix (Important Rule 13 -- never branch HEAD for released versions):

| Tag | quinn-proto version | Source |
|-----|---------------------|--------|
| v0.3.8 | 0.11.9 | `git show v0.3.8:Cargo.lock` |
| v0.3.12 | 0.11.9 | `git show v0.3.12:Cargo.lock` |
| v0.4.5 | 0.11.9 | `git show v0.4.5:Cargo.lock` |
| v0.4.8 | 0.11.12 | `git show v0.4.8:Cargo.lock` |
| v0.4.9 | _(retag of v0.4.8)_ | Carried forward from v0.4.8 (Important Rule 5) |
| v0.4.11 | 0.11.14 | `git show v0.4.11:Cargo.lock` |
| v0.4.12 | 0.11.14 | `git show v0.4.12:Cargo.lock` |

## Version Impact Table

CVE-2026-31812 (quinn-proto < 0.11.14, fixed in 0.11.14):

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.1.1 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.0 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.1 | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.2 | 0.11.12 | YES | retag of 2.2.1 -- same as 2.2.1 |
| 2.2.3 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |

All versions from both streams are included in the impact table (Important Rule 4). Version 2.2.2 is a retag of 2.2.1 with the same backend source commit (v0.4.8), so the affected status is carried forward (Important Rule 5).

## Dependency Chain Context

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) -> reqwest [features: http3] -> h3 -> quinn -> quinn-proto
  Profile: production (reqwest is a runtime dependency)
  Type: transitive dependency
```
