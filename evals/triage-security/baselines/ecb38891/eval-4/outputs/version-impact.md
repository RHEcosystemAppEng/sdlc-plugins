# Step 2 -- Version Impact Analysis

## Step 2.1 -- Supportability Matrix

Loaded security-matrix.md files for both configured version streams:

- **Stream 2.1.x** (rhtpa-release.0.3.z): 2 versions (2.1.0, 2.1.1)
- **Stream 2.2.x** (rhtpa-release.0.4.z): 5 versions (2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4)

Since the issue is **unscoped** (no stream suffix), ALL versions across ALL streams
are included in the analysis.

## Step 2.3 -- Dependency Version Extraction

Extracted h2 versions from Cargo.lock at each pinned commit tag:

| Version | Stream | Pinned Tag | h2 version | Source |
|---------|--------|------------|------------|--------|
| 2.1.0   | 2.1.x  | `v0.3.8`   | 0.4.5      | `git show v0.3.8:Cargo.lock` |
| 2.1.1   | 2.1.x  | `v0.3.12`  | 0.4.5      | `git show v0.3.12:Cargo.lock` |
| 2.2.0   | 2.2.x  | `v0.4.5`   | 0.4.8      | `git show v0.4.5:Cargo.lock` |
| 2.2.1   | 2.2.x  | `v0.4.8`   | 0.4.8      | `git show v0.4.8:Cargo.lock` |
| 2.2.2   | 2.2.x  | `v0.4.9`   | --         | retag of 2.2.1 (backend same as v0.4.8) |
| 2.2.3   | 2.2.x  | `v0.4.11`  | 0.4.9      | `git show v0.4.11:Cargo.lock` |
| 2.2.4   | 2.2.x  | `v0.4.12`  | 0.4.9      | `git show v0.4.12:Cargo.lock` |

## Step 2.4 -- Version Impact Table

Version Impact for CVE-2026-33501 (h2 < 0.4.8):

| Version | Stream | h2 version | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0   | 2.1.x  | 0.4.5      | **YES**   | 0.4.5 < 0.4.8 |
| 2.1.1   | 2.1.x  | 0.4.5      | **YES**   | 0.4.5 < 0.4.8 |
| 2.2.0   | 2.2.x  | 0.4.8      | NO        | 0.4.8 is the fixed version |
| 2.2.1   | 2.2.x  | 0.4.8      | NO        | 0.4.8 is the fixed version |
| 2.2.2   | 2.2.x  | --         | NO        | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3   | 2.2.x  | 0.4.9      | NO        | 0.4.9 >= 0.4.8 |
| 2.2.4   | 2.2.x  | 0.4.9      | NO        | 0.4.9 >= 0.4.8 |

### Summary

- **Stream 2.1.x**: ALL versions affected (2.1.0, 2.1.1 ship h2 0.4.5)
- **Stream 2.2.x**: NO versions affected (all versions ship h2 >= 0.4.8)

The impact is split across streams: stream 2.1.x requires remediation while
stream 2.2.x already ships the patched dependency version.

## Step 2.3.5 -- Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> h2
  Type: direct dependency (present in Cargo.lock as a direct workspace dependency)
  Profile: production (h2 is a runtime dependency for HTTP/2 support)

Remediation: bump h2 to >= 0.4.8 in Cargo.toml on release/0.3.z branch
```

## Step 2.5 -- Upstream Fix Check

| Stream | Ecosystem | Upstream Branch | h2 at HEAD | Fixed? |
|--------|-----------|-----------------|------------|--------|
| 2.1.x  | Cargo     | release/0.3.z   | _(to be checked via git show)_ | _(pending)_ |
| 2.2.x  | Cargo     | release/0.4.z   | 0.4.8+     | YES (already fixed in all released versions) |

Stream 2.2.x already ships the fix in all released versions. Remediation is
required only for stream 2.1.x.
