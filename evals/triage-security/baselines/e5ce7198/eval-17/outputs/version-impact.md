# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Aggregated Supportability Matrix

Data loaded from two stream security matrices:

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | v0.3.8 | |
| 2.1.1 | 0.3.12 | 2025-11-20 | v0.3.12 | |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 | |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 | |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 | |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 | |

## Dependency Version Extraction

Fix threshold: quinn-proto >= 0.11.14 (from Jira description, cross-validated against CVE record).

Ecosystem: **Cargo** (Rust crate)
Lock file: `Cargo.lock`
Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`

### Extracted versions (simulated git show output)

| Tag | quinn-proto version | Source |
|-----|---------------------|--------|
| v0.3.8 | 0.11.9 | git show v0.3.8:Cargo.lock |
| v0.3.12 | 0.11.9 | git show v0.3.12:Cargo.lock |
| v0.4.5 | 0.11.9 | git show v0.4.5:Cargo.lock |
| v0.4.8 | 0.11.12 | git show v0.4.8:Cargo.lock |
| v0.4.9 | _(retag of v0.4.8)_ | skipped -- same as v0.4.8 |
| v0.4.11 | 0.11.14 | git show v0.4.11:Cargo.lock |
| v0.4.12 | 0.11.14 | git show v0.4.12:Cargo.lock |

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | 2.1.x | 0.11.9 | YES | < 0.11.14 |
| 2.2.0 | 2.2.x | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 2.2.x | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | >= 0.11.14, fixed |
| 2.2.4 | 2.2.x | 0.11.14 | NO | >= 0.11.14, fixed |

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) -> reqwest [features: http3] -> h3 -> quinn -> quinn-proto
  Profile: production (reqwest is a runtime dependency)

  quinn-proto is a transitive dependency, pulled in via the http3 feature
  of reqwest. A direct version bump of quinn-proto in Cargo.lock is needed,
  or alternatively updating quinn (which depends on quinn-proto).

First affected: 2.1.0 (v0.3.8) -- quinn-proto 0.11.9
Fixed in: 2.2.3 (v0.4.11) -- quinn-proto updated to 0.11.14
```

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | (not checked -- out of issue scope, but noted for cross-stream impact) | Unknown |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (per v0.4.11+ data) | YES |

The upstream fix is already present on `release/0.4.z` as of v0.4.11. Versions 2.2.3 and 2.2.4 already ship the fixed version. Versions 2.2.0, 2.2.1, and 2.2.2 are affected.

## Cross-Stream Impact Summary

This issue is scoped to **stream 2.2.x** (per the `[rhtpa-2.2]` suffix). However, version impact analysis shows that stream **2.1.x** is also affected (versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9). This cross-stream impact will be reported in Step 7 (Case B).

## Proposed Actions

- Correct Affects Versions from `RHTPA 2.0.0` to `RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2` (scoped to 2.2.x stream)
- Create remediation tasks for affected 2.2.x versions (2.2.0, 2.2.1, 2.2.2)
- Report cross-stream impact for 2.1.x stream
