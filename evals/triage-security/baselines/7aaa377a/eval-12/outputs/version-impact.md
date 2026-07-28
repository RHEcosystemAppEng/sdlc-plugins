# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix

Loaded security-matrix.md for both configured version streams.

### Stream 2.2.x (rhtpa-release.0.4.z) -- in scope per issue suffix [rhtpa-2.2]

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

### Stream 2.1.x (rhtpa-release.0.3.z) -- out of scope but checked for cross-stream impact

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |

## 2.3 -- Dependency Version Extraction

**Fix threshold used**: **0.4.8** (enriched from Step 1.5 cross-validated external CVE data -- MITRE and OSV.dev agreement; NOT from the imprecise Jira description)

Ecosystem: Cargo. Lock file: `Cargo.lock`. Library: h2.

Dependency versions extracted from lock file data at each pinned commit tag:

### Stream 2.2.x (in scope)

| Version | Pinned Commit Tag | h2 version | Affected? (< 0.4.8) | Notes |
|---------|-------------------|------------|----------------------|-------|
| 2.2.0 | `v0.4.5` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.2.1 | `v0.4.8` | 0.4.8 | NO | 0.4.8 is not < 0.4.8 |
| 2.2.2 | `v0.4.8` | -- | NO | retag of 2.2.1; same as 2.2.1 |
| 2.2.3 | `v0.4.11` | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.4 | `v0.4.12` | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

### Stream 2.1.x (cross-stream check)

| Version | Pinned Commit Tag | h2 version | Affected? (< 0.4.8) | Notes |
|---------|-------------------|------------|----------------------|-------|
| 2.1.0 | `v0.3.8` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.1 | `v0.3.12` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |

## Version Impact Summary Table

Version Impact for CVE-2026-48901 (h2 < 0.4.8):

| Version | Stream | h2 version | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.4.5 | YES | cross-stream |
| 2.1.1 | 2.1.x | 0.4.5 | YES | cross-stream |
| 2.2.0 | 2.2.x | 0.4.5 | YES | |
| 2.2.1 | 2.2.x | 0.4.8 | NO | |
| 2.2.2 | 2.2.x | -- | NO | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.4.9 | NO | |
| 2.2.4 | 2.2.x | 0.4.9 | NO | |

**Key finding**: The enriched fix threshold (0.4.8) from Step 1.5 was used for all version impact comparisons. The imprecise Jira description data ("versions prior to the fix") was not usable for automated comparison -- Step 1.5 enrichment was essential for this triage.

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for h2:
  backend (workspace) -> h2
  Type: direct dependency
  Profile: production (h2 is a runtime dependency)

Remediation: bump h2 to >= 0.4.8 in Cargo.toml / Cargo.lock
```

## 2.5 -- Upstream Fix Check

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | Fix available (versions 2.2.1+ already ship h2 >= 0.4.8) |
| 2.1.x | Cargo | release/0.3.z | Requires upstream backport (all versions ship h2 0.4.5) |
