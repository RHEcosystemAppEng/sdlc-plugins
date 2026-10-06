# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Evidence

Lock file inspection performed via `git show <tag>:Cargo.lock` for each pinned
build tag from the supportability matrix. Version 2.2.2 is a retag of 2.2.1
(backend retag, identical source at v0.4.8), so its quinn-proto version is
carried forward from 2.2.1 (0.11.12).

## Affected Version Summary

- **2.1.x stream**: ALL versions affected (2.1.0, 2.1.1) -- quinn-proto 0.11.9
- **2.2.x stream**: 3 of 5 versions affected (2.2.0, 2.2.1, 2.2.2) -- quinn-proto 0.11.9 to 0.11.12
- **2.2.x stream**: 2 versions NOT affected (2.2.3, 2.2.4) -- quinn-proto 0.11.14 (fixed)

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | (needs inspection) | Unknown |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (per v0.4.11+) | YES |

The 2.2.x stream has the fix available upstream (versions 2.2.3+ already ship
quinn-proto 0.11.14). The 2.1.x stream upstream branch needs inspection, but
given that the latest 2.1.x build (v0.3.12) ships quinn-proto 0.11.9, an
upstream backport may be needed on `release/0.3.z`.
