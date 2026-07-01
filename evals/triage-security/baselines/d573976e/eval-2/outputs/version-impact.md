# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix (aggregated)

Loaded from local security-matrix.md files for both configured version streams.

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

## 2.3 -- Dependency Version Extraction

CVE-2026-28940 affects serde_json versions **< 1.0.135**. Fixed version: **1.0.135**.

Extracting serde_json version from `Cargo.lock` at each pinned commit:

### Stream 2.1.x

- **Version 2.1.0** (tag `v0.3.8`): `git show v0.3.8:Cargo.lock | grep -A2 'name = "serde_json"'` -> serde_json **1.0.137**
- **Version 2.1.1** (tag `v0.3.12`): `git show v0.3.12:Cargo.lock | grep -A2 'name = "serde_json"'` -> serde_json **1.0.137**

### Stream 2.2.x

- **Version 2.2.0** (tag `v0.4.5`): `git show v0.4.5:Cargo.lock | grep -A2 'name = "serde_json"'` -> serde_json **1.0.138**
- **Version 2.2.1** (tag `v0.4.8`): `git show v0.4.8:Cargo.lock | grep -A2 'name = "serde_json"'` -> serde_json **1.0.138**
- **Version 2.2.2** (tag `v0.4.8`): backend retag of 2.2.1 -- same source commits as 2.2.1, skipping lock file check. Carrying forward result: serde_json **1.0.138** (same as 2.2.1)
- **Version 2.2.3** (tag `v0.4.11`): `git show v0.4.11:Cargo.lock | grep -A2 'name = "serde_json"'` -> serde_json **1.0.139**
- **Version 2.2.4** (tag `v0.4.12`): `git show v0.4.12:Cargo.lock | grep -A2 'name = "serde_json"'` -> serde_json **1.0.139**

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-28940 (serde_json < 1.0.135):

| Version | Stream | serde_json | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0 | 2.1.x | 1.0.137 | NO | Ships version >= 1.0.135 |
| 2.1.1 | 2.1.x | 1.0.137 | NO | Ships version >= 1.0.135 |
| 2.2.0 | 2.2.x | 1.0.138 | NO | Ships version >= 1.0.135 |
| 2.2.1 | 2.2.x | 1.0.138 | NO | Ships version >= 1.0.135 |
| 2.2.2 | 2.2.x | 1.0.138 | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 1.0.139 | NO | Ships version >= 1.0.135 |
| 2.2.4 | 2.2.x | 1.0.139 | NO | Ships version >= 1.0.135 |

**Result: NO supported versions are affected.** All versions ship serde_json >= 1.0.135, which is at or above the fix threshold. The vulnerable range (< 1.0.135) does not apply to any supported version.

## Dependency Chain Context

Not applicable -- since no versions are affected, dependency chain analysis is not required. For informational context: serde_json is a direct Cargo dependency commonly used for JSON serialization/deserialization in Rust projects.

## 2.5 -- Upstream Fix Check

Not applicable -- since no versions are affected by the vulnerable range, upstream fix status does not need to be evaluated. All shipped versions already include serde_json >= 1.0.135 (the fix threshold).
