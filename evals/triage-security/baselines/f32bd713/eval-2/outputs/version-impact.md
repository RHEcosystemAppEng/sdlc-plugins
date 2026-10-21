# Version Impact Analysis — TC-8002

## CVE-2026-28940: serde_json (affected versions < 1.0.135, fixed in 1.0.135)

### Step 2.1: Supportability Matrix

Loaded from two streams configured in Security Configuration:

- **2.1.x** stream (rhtpa-release.0.3.z): versions 2.1.0, 2.1.1
- **2.2.x** stream (rhtpa-release.0.4.z): versions 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4

### Step 2.3: Dependency Version Extraction

Lock file data extracted via `git show <tag>:Cargo.lock | grep -A2 'name = "serde_json"'`:

| Tag | Version | serde_json version | Source |
|-----|---------|-------------------|--------|
| v0.3.8 | 2.1.0 | 1.0.137 | Cargo.lock at pinned commit |
| v0.3.12 | 2.1.1 | 1.0.137 | Cargo.lock at pinned commit |
| v0.4.5 | 2.2.0 | 1.0.138 | Cargo.lock at pinned commit |
| v0.4.8 | 2.2.1 | 1.0.138 | Cargo.lock at pinned commit |
| v0.4.9 | 2.2.2 | _(retag of v0.4.8)_ | retag -- same as 2.2.1 |
| v0.4.11 | 2.2.3 | 1.0.139 | Cargo.lock at pinned commit |
| v0.4.12 | 2.2.4 | 1.0.139 | Cargo.lock at pinned commit |

### Step 2.4: Version Impact Table

Fix threshold: **1.0.135** (enriched from Step 1.5, consensus across MITRE/OSV/Jira description)

| Version | Stream | serde_json version | Affected? | Notes |
|---------|--------|--------------------|-----------|-------|
| 2.1.0 | 2.1.x | 1.0.137 | **NO** | >= 1.0.135 (ships patched version) |
| 2.1.1 | 2.1.x | 1.0.137 | **NO** | >= 1.0.135 (ships patched version) |
| 2.2.0 | 2.2.x | 1.0.138 | **NO** | >= 1.0.135 (ships patched version) |
| 2.2.1 | 2.2.x | 1.0.138 | **NO** | >= 1.0.135 (ships patched version) |
| 2.2.2 | 2.2.x | 1.0.138 | **NO** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 1.0.139 | **NO** | >= 1.0.135 (ships patched version) |
| 2.2.4 | 2.2.x | 1.0.139 | **NO** | >= 1.0.135 (ships patched version) |

### Summary

**All supported versions ship serde_json >= 1.0.135 (the fix threshold).**

- 2.1.x stream: all versions ship 1.0.137 -- NOT affected
- 2.2.x stream: all versions ship 1.0.138 or 1.0.139 -- NOT affected

No supported versions are affected by CVE-2026-28940. The vulnerability was already fixed before any currently supported version was released.

### Step 2.3.5: Dependency Chain Context

serde_json is a direct, production dependency of the backend workspace (it is a core serialization library used at runtime for JSON processing). However, since no versions are affected, dependency chain analysis is informational only -- no remediation path is needed.

### Step 2.5: Upstream Fix Check

Not applicable -- no versions are affected, so upstream fix status is moot. For completeness: all upstream branches already ship serde_json >= 1.0.135.
