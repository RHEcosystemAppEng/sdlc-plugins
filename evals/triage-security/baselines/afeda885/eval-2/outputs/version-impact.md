# Version Impact Analysis — TC-8002

## CVE-2026-28940: serde_json — versions before 1.0.135

Fix threshold: **1.0.135** (from Jira description; external CVE API enrichment not performed per eval constraints)

## Step 2.3 — Dependency Version Extraction

Dependency versions extracted from `Cargo.lock` at each pinned tag (simulated from mock lock file data):

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | serde_json version | Source |
|---------|-----------|-------------------|--------|
| 2.1.0 | v0.3.8 | 1.0.137 | `git show v0.3.8:Cargo.lock` |
| 2.1.1 | v0.3.12 | 1.0.137 | `git show v0.3.12:Cargo.lock` |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build Tag | serde_json version | Source |
|---------|-----------|-------------------|--------|
| 2.2.0 | v0.4.5 | 1.0.138 | `git show v0.4.5:Cargo.lock` |
| 2.2.1 | v0.4.8 | 1.0.138 | `git show v0.4.8:Cargo.lock` |
| 2.2.2 | v0.4.9 | _(retag of v0.4.8)_ | same as 2.2.1 |
| 2.2.3 | v0.4.11 | 1.0.139 | `git show v0.4.11:Cargo.lock` |
| 2.2.4 | v0.4.12 | 1.0.139 | `git show v0.4.12:Cargo.lock` |

## Step 2.4 — Version Impact Table

Version Impact for CVE-2026-28940 (serde_json < 1.0.135):

| Version | Stream | serde_json | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0 | 2.1.x | 1.0.137 | **NO** | ships 1.0.137 >= 1.0.135 fix threshold |
| 2.1.1 | 2.1.x | 1.0.137 | **NO** | ships 1.0.137 >= 1.0.135 fix threshold |
| 2.2.0 | 2.2.x | 1.0.138 | **NO** | ships 1.0.138 >= 1.0.135 fix threshold |
| 2.2.1 | 2.2.x | 1.0.138 | **NO** | ships 1.0.138 >= 1.0.135 fix threshold |
| 2.2.2 | 2.2.x | — | **NO** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 1.0.139 | **NO** | ships 1.0.139 >= 1.0.135 fix threshold |
| 2.2.4 | 2.2.x | 1.0.139 | **NO** | ships 1.0.139 >= 1.0.135 fix threshold |

### Summary

**No supported version is affected.** Every version across both streams ships serde_json >= 1.0.135, which is at or above the fix threshold. The earliest version (2.1.0, built 2025-09-15) already ships serde_json 1.0.137, meaning the vulnerable versions (before 1.0.135) were never included in any supported product release.

## Step 2.3.5 — Dependency Chain Context

Not applicable. Since no version is affected (all ship a patched version of serde_json), dependency chain tracing is not required for remediation planning.

## Step 2.5 — Upstream Fix Status

Not applicable. Since no supported version ships the vulnerable dependency, upstream fix status analysis is moot. All versions already include the fix.
