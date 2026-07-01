# Step 2 -- Version Impact Analysis

## Step 0.3 -- Matrix Staleness Check

The security-matrix.md has `Last-Updated: 2026-06-28T10:00:00Z`. Current date is 2026-07-01. The matrix is 3 days old, which is within the 14-day default threshold. Proceeding without staleness warning.

## Supportability Matrix

Data loaded from security-matrix.md for both configured Version Streams.

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## Version Impact Table

Version impact analysis for CVE-2026-31812 (quinn-proto < 0.11.14):

All dependency versions are extracted from lock files at the **pinned commit tags** from the supportability matrix (Important Rule 13), not from branch HEAD.

| Version | Stream | Pinned Tag | quinn-proto version | Affected? | Notes |
|---------|--------|------------|---------------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | **YES** | 0.11.12 < 0.11.14 |
| 2.2.2 | 2.2.x | `v0.4.8` | -- | **YES** | retag of 2.2.1 (same backend tag `v0.4.8`); same as 2.2.1 |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |

### Summary

- **Affected versions**: 2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2
- **Not affected versions**: 2.2.3, 2.2.4
- **Retag handling**: Version 2.2.2 is a retag of 2.2.1 (identical backend tag `v0.4.8`). Lock file check was skipped; affected status carried forward from 2.2.1 per Important Rule 5.

### Dependency Chain Context

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) -> quinn -> quinn-proto
  Ecosystem: Cargo (source dependency)
  Lock file: Cargo.lock
  Profile: production (quinn is a runtime dependency)

  First appeared in affected range: present in all checked versions (v0.3.8 onward)
  Fixed in: v0.4.11 (version 2.2.3, quinn-proto bumped to 0.11.14)
```

## Upstream Fix Check

| Stream | Ecosystem | Upstream Branch | Notes |
|--------|-----------|-----------------|-------|
| 2.1.x | Cargo | `release/0.3.z` | Upstream fix PR: quinn-rs/quinn#2048 |
| 2.2.x | Cargo | `release/0.4.z` | Upstream fix PR: quinn-rs/quinn#2048 |

The upstream fix PR (https://github.com/quinn-rs/quinn/pull/2048) is available. Versions 2.2.3+ already ship the fix (quinn-proto 0.11.14).
