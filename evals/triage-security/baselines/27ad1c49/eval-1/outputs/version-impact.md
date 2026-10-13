# Version Impact Analysis — CVE-2026-31812 (quinn-proto)

## Step 2.1 — Supportability Matrix

Two version streams loaded from security-matrix.md:

**Stream 2.1.x** (rhtpa-release.0.3.z):

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |

**Stream 2.2.x** (rhtpa-release.0.4.z):

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

Source pinning method for both streams: `artifacts.lock.yaml` (download URL
contains tag).

Ecosystem mappings used for inspection:

| Stream | Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|--------|-----------|------------|-----------|---------------|-----------------|
| 2.1.x | Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| 2.2.x | Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

## Step 2.3 — Dependency Version Extraction

Fix threshold: **0.11.14** (from Jira description; external enrichment via
MITRE/OSV would be performed in interactive mode for cross-validation).

Extracted quinn-proto versions from `Cargo.lock` at each pinned commit:

| Version | Stream | Tag | quinn-proto version | Affected? (< 0.11.14) |
|---------|--------|-----|--------------------|-----------------------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | **YES** |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | **YES** |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | **YES** |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | **YES** |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | **YES** | retag of 2.2.1 (same as 2.2.1: 0.11.12) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | **NO** |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | **NO** |

## Step 2.3.5 — Dependency Chain Context

Dependency chain analysis for quinn-proto in the backend repository requires
inspecting `Cargo.toml` workspace members at the pinned commits. In interactive
mode, the following commands would determine direct vs. transitive status:

```bash
git show <tag>:Cargo.toml | grep quinn-proto
git show <tag>:Cargo.lock | grep -B5 -A5 'name = "quinn-proto"'
```

Based on the available lock file data, quinn-proto is present in the Cargo.lock
for all versions. The dependency chain (direct vs. transitive) and profile/scope
(production vs. dev-only) would be determined by inspecting the manifest files.
This investigation would be completed before finalizing remediation tasks.

## Step 2.4 — Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | **YES** | |
| 2.1.1 | 2.1.x | 0.11.9 | **YES** | |
| 2.2.0 | 2.2.x | 0.11.9 | **YES** | |
| 2.2.1 | 2.2.x | 0.11.12 | **YES** | |
| 2.2.2 | 2.2.x | -- | **YES** | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | **NO** | >= fix threshold |
| 2.2.4 | 2.2.x | 0.11.14 | **NO** | >= fix threshold |

### Summary by stream

- **2.1.x**: ALL versions affected (2.1.0, 2.1.1)
- **2.2.x**: versions 2.2.0, 2.2.1, 2.2.2 affected; versions 2.2.3, 2.2.4 NOT affected (fix incorporated in 2.2.3, shipped 2026-03-23)

## Step 2.5 — Upstream Fix Status

Upstream fix check for each stream's Cargo ecosystem:

| Stream | Ecosystem | Upstream Branch | Latest Released Version at Branch | Fixed? |
|--------|-----------|-----------------|-----------------------------------|--------|
| 2.1.x | Cargo | `release/0.3.z` | 0.11.9 (at `v0.3.12`) | **NO** |
| 2.2.x | Cargo | `release/0.4.z` | 0.11.14 (at `v0.4.12`) | **YES** |

**Analysis:**

- **2.2.x stream**: The upstream branch `release/0.4.z` already ships quinn-proto
  0.11.14 (the fixed version). This is confirmed by RHTPA 2.2.3 and 2.2.4
  shipping the fix. No new upstream work is needed for 2.2.x. The fix was
  incorporated naturally through the release pipeline without a dedicated
  remediation task.

- **2.1.x stream**: The upstream branch `release/0.3.z` still ships quinn-proto
  0.11.9, which is within the affected range. This stream requires an upstream
  backport to bump quinn-proto to >= 0.11.14. Note: this stream is outside the
  current issue's scope (TC-8001 is scoped to 2.2.x); cross-stream impact is
  handled via Case A in Step 8.
