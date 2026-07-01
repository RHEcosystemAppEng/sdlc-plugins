# Step 2 -- Version Impact Analysis

## 2.1 -- Load the Supportability Matrix

Two streams loaded from security-matrix.md:

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.2 -- Development Stream Detection

(Skipped per eval instructions -- would query Jira for unreleased versions.)

## 2.3 -- Extract Dependency Versions

Fix threshold: **0.11.14** (from Step 1 data extraction, using Jira description data)

Using mock lock file data from the fixture for `quinn-proto` by tag:

| Tag | quinn-proto version | Comparison to threshold (< 0.11.14) |
|-----|---------------------|--------------------------------------|
| `v0.3.8` | 0.11.9 | 0.11.9 < 0.11.14 -- AFFECTED |
| `v0.3.12` | 0.11.9 | 0.11.9 < 0.11.14 -- AFFECTED |
| `v0.4.5` | 0.11.9 | 0.11.9 < 0.11.14 -- AFFECTED |
| `v0.4.8` | 0.11.12 | 0.11.12 < 0.11.14 -- AFFECTED |
| `v0.4.9` | _(retag of v0.4.8)_ | same as v0.4.8 -- AFFECTED |
| `v0.4.11` | 0.11.14 | 0.11.14 >= 0.11.14 -- NOT AFFECTED |
| `v0.4.12` | 0.11.14 | 0.11.14 >= 0.11.14 -- NOT AFFECTED |

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | |

### Dependency Chain Context (Step 2.3.5)

Dependency chain for quinn-proto (Cargo):

```
Dependency chain for quinn-proto:
  backend (workspace) -> [reqwest or similar QUIC dependency] -> quinn -> quinn-proto
  Profile: production (quinn-proto is a runtime dependency for QUIC transport)

  Present in: all versions (2.1.0 through 2.2.4)
  Affected versions: 2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2 (ship quinn-proto < 0.11.14)
  Fixed in: 2.2.3+ (ship quinn-proto 0.11.14)
```

## 2.5 -- Upstream Fix Check

Upstream fix status (from Ecosystem Mappings Upstream Branch column):

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | (would check via `git show release/0.4.z:Cargo.lock`) | (requires git access) |
| 2.1.x | Cargo | release/0.3.z | (would check via `git show release/0.3.z:Cargo.lock`) | (requires git access) |

Note: Upstream fix check requires actual git access which is not available in this eval.
The upstream fix PR (quinn-rs/quinn#2048) is linked in the remote links, confirming a fix exists upstream.

### Cross-Stream Summary

- **Stream 2.1.x**: versions 2.1.0, 2.1.1 are AFFECTED (quinn-proto 0.11.9)
- **Stream 2.2.x**: versions 2.2.0, 2.2.1, 2.2.2 are AFFECTED; versions 2.2.3, 2.2.4 are NOT AFFECTED

Since this issue is scoped to stream 2.2.x (suffix `[rhtpa-2.2]`), Steps 3 and 8 apply only to 2.2.x versions. The 2.1.x impact is noted for cross-stream awareness (Step 8 Case B).
