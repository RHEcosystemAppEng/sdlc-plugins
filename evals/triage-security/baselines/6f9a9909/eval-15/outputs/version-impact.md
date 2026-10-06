# Step 2 — Version Impact Analysis for CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | — | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | fixed at 0.11.14 |
| 2.2.4 | 2.2.x | 0.11.14 | NO | fixed at 0.11.14 |

## Evidence

Dependency versions extracted from `Cargo.lock` at pinned source commits per the supportability matrix:

| Tag | Source | quinn-proto version | Comparison vs fix threshold (0.11.14) |
|-----|--------|---------------------|---------------------------------------|
| v0.3.8 | 2.1.0 backend | 0.11.9 | 0.11.9 < 0.11.14 — AFFECTED |
| v0.3.12 | 2.1.1 backend | 0.11.9 | 0.11.9 < 0.11.14 — AFFECTED |
| v0.4.5 | 2.2.0 backend | 0.11.9 | 0.11.9 < 0.11.14 — AFFECTED |
| v0.4.8 | 2.2.1 backend | 0.11.12 | 0.11.12 < 0.11.14 — AFFECTED |
| v0.4.9 | 2.2.2 backend | _(retag of v0.4.8)_ | same as 2.2.1 — AFFECTED |
| v0.4.11 | 2.2.3 backend | 0.11.14 | 0.11.14 >= 0.11.14 — NOT AFFECTED |
| v0.4.12 | 2.2.4 backend | 0.11.14 | 0.11.14 >= 0.11.14 — NOT AFFECTED |

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (per v0.4.11+) | YES |
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (per v0.3.12) | NO |

The 2.2.x stream was fixed starting from version 2.2.3 (tag v0.4.11, quinn-proto 0.11.14). The 2.1.x stream remains unfixed — upstream branch `release/0.3.z` still ships quinn-proto 0.11.9.

## Cross-Stream Summary

- **2.2.x stream** (this issue's scope): versions 2.2.0, 2.2.1, 2.2.2 are affected; 2.2.3+ are fixed
- **2.1.x stream** (outside this issue's scope): all versions (2.1.0, 2.1.1) are affected — triggers Case A cross-stream impact in Step 8
