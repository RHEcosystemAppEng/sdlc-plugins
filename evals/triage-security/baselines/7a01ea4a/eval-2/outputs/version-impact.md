# Version Impact Analysis -- CVE-2026-28940

## Step 2 -- Version Impact

### Supportability Matrix (Aggregated)

#### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | v0.3.8 | |
| 2.1.1 | 0.3.12 | 2025-11-20 | v0.3.12 | |

#### Stream 2.2.x (rhtpa-release.0.4.z) -- issue-scoped stream

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 | |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 | |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 | |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 | |

### Step 2.3 -- Dependency Version Extraction

serde_json versions extracted from `Cargo.lock` at each pinned commit:

| Tag | serde_json version | Source |
|-----|--------------------|--------|
| v0.3.8 | 1.0.137 | `git show v0.3.8:Cargo.lock` |
| v0.3.12 | 1.0.137 | `git show v0.3.12:Cargo.lock` |
| v0.4.5 | 1.0.138 | `git show v0.4.5:Cargo.lock` |
| v0.4.8 | 1.0.138 | `git show v0.4.8:Cargo.lock` |
| v0.4.9 | _(retag of v0.4.8)_ | same as v0.4.8 |
| v0.4.11 | 1.0.139 | `git show v0.4.11:Cargo.lock` |
| v0.4.12 | 1.0.139 | `git show v0.4.12:Cargo.lock` |

### Version Impact Table

Fix threshold: serde_json >= 1.0.135

| Version | Stream | serde_json | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0 | 2.1.x | 1.0.137 | NO | >= 1.0.135 |
| 2.1.1 | 2.1.x | 1.0.137 | NO | >= 1.0.135 |
| 2.2.0 | 2.2.x | 1.0.138 | NO | >= 1.0.135 |
| 2.2.1 | 2.2.x | 1.0.138 | NO | >= 1.0.135 |
| 2.2.2 | 2.2.x | 1.0.138 | NO | retag of 2.2.1, same as 2.2.1 |
| 2.2.3 | 2.2.x | 1.0.139 | NO | >= 1.0.135 |
| 2.2.4 | 2.2.x | 1.0.139 | NO | >= 1.0.135 |

**Result: NO supported versions are affected.**

All versions across both streams ship serde_json >= 1.0.137, which is well above
the fix threshold of 1.0.135. The vulnerability (affecting versions before 1.0.135)
does not apply to any shipped version.

### Step 2.3.5 -- Dependency Chain Context

Since no version is affected, dependency chain tracing is not required. The
vulnerable version range (< 1.0.135) was never shipped in any supported product
version. The earliest serde_json version found across all streams is 1.0.137
(in stream 2.1.x), which already includes the fix.

### Step 2.5 -- Upstream Fix Status

Not applicable -- no versions are affected. The fix (serde_json 1.0.135) was
already present in the dependency tree before any currently supported product
version was released.
