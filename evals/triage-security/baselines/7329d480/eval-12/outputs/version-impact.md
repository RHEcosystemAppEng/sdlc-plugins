# Step 2 -- Version Impact Analysis

## CVE-2026-48901 (h2 < 0.4.8)

**Enriched fix threshold**: 0.4.8 (from Step 1.5 cross-validation of MITRE CVE API and OSV.dev)
**Ecosystem**: Cargo
**Lock file**: Cargo.lock
**Issue stream scope**: 2.2.x

### Version Impact Table

All supported versions across all streams are checked, regardless of issue scope.

#### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | h2 version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.1 | v0.3.12 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |

#### Stream 2.2.x (rhtpa-release.0.4.z) -- issue scoped stream

| Version | Build Tag | h2 version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.1 | v0.4.8 | 0.4.8 | NO | 0.4.8 >= 0.4.8 |
| 2.2.2 | v0.4.8 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.4 | v0.4.12 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

### Summary

| Stream | Affected versions | Unaffected versions |
|--------|-------------------|---------------------|
| 2.1.x | 2.1.0, 2.1.1 | None |
| 2.2.x (scoped) | None | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 |

**Scoped stream (2.2.x)**: NO versions are affected. All 2.2.x releases ship h2 >= 0.4.8, which is at or above the fix threshold.

**Other stream (2.1.x)**: ALL versions are affected. Both 2.1.x releases ship h2 0.4.5, which is below the fix threshold.

### Dependency Chain Context

Dependency chain for h2 (Cargo):

The h2 crate is a Rust HTTP/2 implementation. Based on the Cargo ecosystem mappings, it is a dependency within the backend repository.

- Ecosystem: Cargo (crates.io)
- Lock file: Cargo.lock
- Repository: backend

Present in: all streams (2.1.x at 0.4.5, 2.2.x at 0.4.8+)
The dependency ships in all product versions but only 2.1.x versions include the vulnerable range.

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Check Command | Notes |
|--------|-----------|-----------------|---------------|-------|
| 2.1.x | Cargo | release/0.3.z | `git show release/0.3.z:Cargo.lock` | Needs verification |
| 2.2.x | Cargo | release/0.4.z | `git show release/0.4.z:Cargo.lock` | Already ships fixed h2 (0.4.8+) |

The 2.2.x stream already ships the fixed h2 version in all releases. The 2.1.x stream ships h2 0.4.5, which is vulnerable and requires remediation.

### Affects Versions Assessment

**PSIRT-assigned Affects Versions**: RHTPA 2.2.0

**Lock file evidence**: RHTPA 2.2.0 ships h2 0.4.8, which is NOT affected (at fix threshold).

**Conclusion**: The PSIRT-assigned Affects Versions is **incorrect**. Version 2.2.0 is not affected based on lock file analysis. No 2.2.x versions are affected. The affected versions are in the 2.1.x stream (2.1.0 and 2.1.1), which is outside this issue's scope.
