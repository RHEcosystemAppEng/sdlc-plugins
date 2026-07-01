# Step 2 -- Version Impact Analysis

## 2.1 -- Load supportability matrix

Loaded security-matrix.md covering two version streams:
- **Stream 2.1.x** (rhtpa-release.0.3.z): versions 2.1.0, 2.1.1
- **Stream 2.2.x** (rhtpa-release.0.4.z): versions 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4

Matrix `Last-Updated` timestamp: 2026-06-28T10:00:00Z (fresh, within 14-day threshold).

## 2.2 -- Detect development stream

(Would query Jira for unreleased versions matching prefix RHTPA. In this eval, no development stream data is available from fixtures. Proceeding with released versions only.)

## 2.3 -- Extract dependency versions

**Enriched fix threshold from Step 1.5**: h2 < **0.4.8** is affected.

This threshold was obtained from cross-validated MITRE CVE API and OSV.dev data (both report fixed at 0.4.8). The imprecise Jira description ("versions prior to the fix" / "see advisory") was insufficient -- the enriched threshold is used as the authoritative value for all comparisons below.

### Stream 2.2.x (scoped -- primary analysis)

Using Ecosystem Mappings: Cargo, Repository: backend, Lock File: `Cargo.lock`, Check Command: `git show <tag>:Cargo.lock`

| Version | Tag | h2 version (from lock file) | Affected? (< 0.4.8) | Notes |
|---------|-----|-----------------------------|----------------------|-------|
| 2.2.0 | `v0.4.5` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.2.1 | `v0.4.8` | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.2 | `v0.4.9` | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | `v0.4.11` | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.4 | `v0.4.12` | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

### Stream 2.1.x (cross-stream awareness -- not in scope for Affects Versions, but checked per Important Rule 4)

| Version | Tag | h2 version (from lock file) | Affected? (< 0.4.8) | Notes |
|---------|-----|-----------------------------|----------------------|-------|
| 2.1.0 | `v0.3.8` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.1 | `v0.3.12` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |

## 2.4 -- Version Impact Table (combined)

Version Impact for CVE-2026-48901 (h2 < 0.4.8):

| Version | Stream | h2 version | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.4.5 | YES | |
| 2.1.1 | 2.1.x | 0.4.5 | YES | |
| 2.2.0 | 2.2.x | 0.4.5 | YES | |
| 2.2.1 | 2.2.x | 0.4.8 | NO | at fix threshold |
| 2.2.2 | 2.2.x | -- | NO | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.4.9 | NO | |
| 2.2.4 | 2.2.x | 0.4.9 | NO | |

**Key finding**: The enriched fix threshold (0.4.8) from Step 1.5 was essential for this analysis. Without external CVE data, the imprecise Jira description ("versions prior to the fix") would not have provided a usable comparison value for version impact determination.

### Dependency chain context (Step 2.3.5)

Dependency chain for h2 (Cargo):
- h2 is a Cargo (Rust) crate used for HTTP/2 protocol support
- Based on the Cargo ecosystem, h2 is likely a transitive dependency pulled in through a higher-level HTTP stack (e.g., hyper -> h2)
- Profile: production (h2 is a runtime dependency for HTTP/2 communication)

For affected version 2.2.0 (tag v0.4.5): h2 0.4.5 is present in the lock file.
For non-affected versions 2.2.1+ (tags v0.4.8+): h2 has been updated to 0.4.8+ which is at or above the fix threshold.

## 2.5 -- Upstream fix check

Using Ecosystem Mappings for stream 2.2.x: Upstream Branch = `release/0.4.z`, Repository: backend

(Would run: `git -C /home/dev/repos/rhtpa-backend show release/0.4.z:Cargo.lock | grep -A2 'name = "h2"'`)

Based on the latest released version (2.2.4, tag v0.4.12) shipping h2 0.4.9 (which is >= 0.4.8), it is highly likely that the upstream branch `release/0.4.z` already has the fix.

Upstream fix status:

| Stream | Ecosystem | Upstream Branch | Latest Released Version at HEAD | Fixed? |
|--------|-----------|-----------------|----------------------------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.4.9 (from v0.4.12) | YES (likely) |
| 2.1.x | Cargo | release/0.3.z | 0.4.5 (from v0.3.12) | NO |

**Proposed action**: Present version impact table to engineer for confirmation before proceeding to Step 3.
