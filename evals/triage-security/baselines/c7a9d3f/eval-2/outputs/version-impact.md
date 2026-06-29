# Version Impact Analysis -- TC-8002

## CVE-2026-28940: serde_json (affected: versions before 1.0.135, fixed: 1.0.135)

### Aggregated Supportability Matrix

**Stream 2.1.x** (rhtpa-release.0.3.z):

| Version | Build | Build Date | backend tag |
|---------|-------|------------|-------------|
| 2.1.0 | 0.3.8 | 2025-09-15 | v0.3.8 |
| 2.1.1 | 0.3.12 | 2025-11-20 | v0.3.12 |

**Stream 2.2.x** (rhtpa-release.0.4.z):

| Version | Build | Build Date | backend tag |
|---------|-------|------------|-------------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 (retag of 2.2.1) |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 |

### Lock File Evidence (serde_json versions by pinned commit)

| Tag | serde_json version | Source |
|-----|-------------------|--------|
| v0.3.8 | 1.0.137 | Cargo.lock at v0.3.8 |
| v0.3.12 | 1.0.137 | Cargo.lock at v0.3.12 |
| v0.4.5 | 1.0.138 | Cargo.lock at v0.4.5 |
| v0.4.8 | 1.0.138 | Cargo.lock at v0.4.8 |
| v0.4.9 | (retag of v0.4.8) | same as v0.4.8 |
| v0.4.11 | 1.0.139 | Cargo.lock at v0.4.11 |
| v0.4.12 | 1.0.139 | Cargo.lock at v0.4.12 |

### Version Impact Table

Fix threshold: serde_json >= 1.0.135 (not affected if version is 1.0.135 or later)

| Version | Stream | serde_json version | Affected? | Notes |
|---------|--------|--------------------|-----------|-------|
| 2.1.0 | 2.1.x | 1.0.137 | **NO** | >= 1.0.135 |
| 2.1.1 | 2.1.x | 1.0.137 | **NO** | >= 1.0.135 |
| 2.2.0 | 2.2.x | 1.0.138 | **NO** | >= 1.0.135 |
| 2.2.1 | 2.2.x | 1.0.138 | **NO** | >= 1.0.135 |
| 2.2.2 | 2.2.x | 1.0.138 | **NO** | retag of 2.2.1; same as 2.2.1 |
| 2.2.3 | 2.2.x | 1.0.139 | **NO** | >= 1.0.135 |
| 2.2.4 | 2.2.x | 1.0.139 | **NO** | >= 1.0.135 |

### Summary

**No supported versions are affected.** Every version across both streams (2.1.x and 2.2.x) ships serde_json >= 1.0.137, which is above the fix threshold of 1.0.135. The vulnerability was already remediated before any supported product version was built.

- Lowest serde_json version shipped: **1.0.137** (in 2.1.0 and 2.1.1, built 2025-09-15 and 2025-11-20)
- Fix threshold: **1.0.135**
- All shipped versions exceed the fix threshold by at least 2 patch releases
