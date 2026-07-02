# Step 2 -- Version Impact Analysis: CVE-2026-28940

## Supportability Matrix (aggregated from all streams)

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | backend tag |
|---------|-------|------------|-------------|
| 2.1.0 | 0.3.8 | 2025-09-15 | v0.3.8 |
| 2.1.1 | 0.3.12 | 2025-11-20 | v0.3.12 |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 | |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 | |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 | |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 | |

## Dependency Version Extraction

Fix threshold: serde_json >= 1.0.135 (from CVE data; affected range is versions before 1.0.135).

Extracted serde_json versions from `Cargo.lock` at each pinned tag:

| Tag | serde_json version | Source |
|-----|--------------------|--------|
| v0.3.8 | 1.0.137 | `git show v0.3.8:Cargo.lock` |
| v0.3.12 | 1.0.137 | `git show v0.3.12:Cargo.lock` |
| v0.4.5 | 1.0.138 | `git show v0.4.5:Cargo.lock` |
| v0.4.8 | 1.0.138 | `git show v0.4.8:Cargo.lock` |
| v0.4.9 | _(retag of v0.4.8)_ | same as v0.4.8 |
| v0.4.11 | 1.0.139 | `git show v0.4.11:Cargo.lock` |
| v0.4.12 | 1.0.139 | `git show v0.4.12:Cargo.lock` |

## Version Impact Table

Version Impact for CVE-2026-28940 (serde_json < 1.0.135):

| Version | Stream | serde_json | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0 | 2.1.x | 1.0.137 | NO | >= 1.0.135 fix threshold |
| 2.1.1 | 2.1.x | 1.0.137 | NO | >= 1.0.135 fix threshold |
| 2.2.0 | 2.2.x | 1.0.138 | NO | >= 1.0.135 fix threshold |
| 2.2.1 | 2.2.x | 1.0.138 | NO | >= 1.0.135 fix threshold |
| 2.2.2 | 2.2.x | 1.0.138 | NO | retag of 2.2.1, same as 2.2.1 |
| 2.2.3 | 2.2.x | 1.0.139 | NO | >= 1.0.135 fix threshold |
| 2.2.4 | 2.2.x | 1.0.139 | NO | >= 1.0.135 fix threshold |

**Result: NO supported versions are affected.** All shipped versions of serde_json (1.0.137, 1.0.138, 1.0.139) are at or above the fix threshold of 1.0.135. The vulnerable range (versions before 1.0.135) is not present in any supported product version.

## Upstream Fix Status

Not applicable -- no versions are affected, so upstream fix status is moot. For completeness, all upstream branches already carry serde_json versions well above the fix threshold.
