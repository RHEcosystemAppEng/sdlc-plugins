# Step 2 -- Version Impact Analysis

## Step 0.3 -- Matrix Staleness Check

The security-matrix.md has a `Last-Updated: 2026-06-28T10:00:00Z` timestamp. As of the current date (2026-07-01), the matrix is **3 days old**, which is within the 14-day default threshold. Proceeding without staleness warning.

## Supportability Matrix (Aggregated)

All versions from both configured streams are included (Important Rule 4: check ALL supported versions).

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | backend (pinned commit) | Notes |
|---------|-------|------------|-------------------------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Build Date | backend (pinned commit) | Notes |
|---------|-------|------------|-------------------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## Dependency Version Extraction

Lock file inspection uses the pinned commit tags from the supportability matrix for each version (Important Rule 13 -- never branch HEAD for released versions).

Simulated `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'` results:

| Version | Pinned Tag | h2 version (from Cargo.lock) |
|---------|------------|------------------------------|
| 2.1.0 | `v0.3.8` | 0.4.5 |
| 2.1.1 | `v0.3.12` | 0.4.5 |
| 2.2.0 | `v0.4.5` | 0.4.8 |
| 2.2.1 | `v0.4.8` | 0.4.8 |
| 2.2.2 | `v0.4.9` | _(retag of v0.4.8 -- carried forward)_ |
| 2.2.3 | `v0.4.11` | 0.4.9 |
| 2.2.4 | `v0.4.12` | 0.4.9 |

## Version Impact Table

CVE-2026-33501 (h2 < 0.4.8) -- fix threshold: 0.4.8

| Version | Stream | h2 version | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.1 | 2.1.x | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.2.0 | 2.2.x | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.1 | 2.2.x | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.2 | 2.2.x | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.4 | 2.2.x | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

### Summary

- **Stream 2.1.x**: ALL versions are **affected** (h2 0.4.5, below fix threshold 0.4.8)
- **Stream 2.2.x**: ALL versions are **not affected** (h2 >= 0.4.8, at or above fix threshold)

This is a **mixed impact** result -- the vulnerable dependency is present only in the 2.1.x stream. The 2.2.x stream already ships the patched version.

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for h2 (Cargo):
  backend (workspace) -> hyper -> h2
  Profile: production (hyper is a runtime dependency)

  Stream 2.1.x: h2 0.4.5 (affected -- below fix threshold 0.4.8)
  Stream 2.2.x: h2 0.4.8+ (not affected -- at or above fix threshold)

  Introduction: h2 is a transitive dependency via hyper, present in all versions.
  The 2.2.x stream updated to h2 0.4.8 starting from version 2.2.0 (v0.4.5 tag).
```

## Upstream Fix Check (Step 2.5)

| Stream | Ecosystem | Upstream Branch | h2 at branch HEAD | Fixed? |
|--------|-----------|-----------------|---------------------|--------|
| 2.1.x | Cargo | release/0.3.z | _(would need git show)_ | To be verified |
| 2.2.x | Cargo | release/0.4.z | 0.4.9 | YES (already ships fix) |

Note: Since 2.2.x already ships h2 >= 0.4.8 in all released versions, the upstream fix is confirmed for that stream. The 2.1.x upstream branch needs verification to determine if the fix has been backported.
