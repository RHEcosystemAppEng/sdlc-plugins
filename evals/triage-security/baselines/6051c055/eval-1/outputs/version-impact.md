# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | ships fixed version |

## Evidence

Dependency versions extracted from lock files at pinned source commits:

| Tag | Source | quinn-proto version | Compared to fix threshold (0.11.14) |
|-----|--------|---------------------|-------------------------------------|
| `v0.3.8` (2.1.0) | `git show v0.3.8:Cargo.lock` | 0.11.9 | 0.11.9 < 0.11.14 -- AFFECTED |
| `v0.3.12` (2.1.1) | `git show v0.3.12:Cargo.lock` | 0.11.9 | 0.11.9 < 0.11.14 -- AFFECTED |
| `v0.4.5` (2.2.0) | `git show v0.4.5:Cargo.lock` | 0.11.9 | 0.11.9 < 0.11.14 -- AFFECTED |
| `v0.4.8` (2.2.1) | `git show v0.4.8:Cargo.lock` | 0.11.12 | 0.11.12 < 0.11.14 -- AFFECTED |
| `v0.4.9` (2.2.2) | skipped -- retag of v0.4.8 | (same as 2.2.1) | AFFECTED (carried forward) |
| `v0.4.11` (2.2.3) | `git show v0.4.11:Cargo.lock` | 0.11.14 | 0.11.14 >= 0.11.14 -- NOT AFFECTED |
| `v0.4.12` (2.2.4) | `git show v0.4.12:Cargo.lock` | 0.11.14 | 0.11.14 >= 0.11.14 -- NOT AFFECTED |

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (assumed based on presence in Cargo.lock)
  Profile: production (quinn-proto is a runtime QUIC protocol dependency)
  Ecosystem: Cargo

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | (check required) | TBD |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (per v0.4.11+) | YES |

The 2.2.x stream's upstream branch (`release/0.4.z`) already contains the fix -- versions 2.2.3+ ship quinn-proto 0.11.14. Remediation for 2.2.x is a downstream-only propagation: update the source reference in the Konflux release repo to point to a tag that includes the fix (v0.4.11 or later).

For the 2.1.x stream (`release/0.3.z`), the latest pinned tag (v0.3.12) still ships quinn-proto 0.11.9. An upstream backport to the `release/0.3.z` branch is required before downstream propagation.

## Summary

- **2.2.x stream (issue scope):** Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship the fix.
- **2.1.x stream (cross-stream):** All versions (2.1.0, 2.1.1) are affected. This will be reported via Case B cross-stream impact.
