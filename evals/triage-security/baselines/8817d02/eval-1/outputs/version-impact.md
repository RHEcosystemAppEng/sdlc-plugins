# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix

Loaded from two streams configured in the Version Streams table:

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

## 2.3 -- Dependency Version Extraction

Using the mock lock file data, the following quinn-proto versions were extracted per tag:

| Tag | quinn-proto version | Method |
|-----|---------------------|--------|
| `v0.3.8` | 0.11.9 | `git show v0.3.8:Cargo.lock \| grep -A2 'name = "quinn-proto"'` |
| `v0.3.12` | 0.11.9 | `git show v0.3.12:Cargo.lock \| grep -A2 'name = "quinn-proto"'` |
| `v0.4.5` | 0.11.9 | `git show v0.4.5:Cargo.lock \| grep -A2 'name = "quinn-proto"'` |
| `v0.4.8` | 0.11.12 | `git show v0.4.8:Cargo.lock \| grep -A2 'name = "quinn-proto"'` |
| `v0.4.9` | _(retag of v0.4.8)_ | Skipped -- same as v0.4.8 |
| `v0.4.11` | 0.11.14 | `git show v0.4.11:Cargo.lock \| grep -A2 'name = "quinn-proto"'` |
| `v0.4.12` | 0.11.14 | `git show v0.4.12:Cargo.lock \| grep -A2 'name = "quinn-proto"'` |

CVE-2026-31812 affected range: **versions before 0.11.14** (< 0.11.14). Fixed in **0.11.14**.

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | 2.1.x | 0.11.9 | YES | < 0.11.14 |
| 2.2.0 | 2.2.x | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 2.2.x | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as 2.2.1: 0.11.12) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | >= 0.11.14 (fixed version) |
| 2.2.4 | 2.2.x | 0.11.14 | NO | >= 0.11.14 (fixed version) |

### Dependency Chain Context (Step 2.3.5)

Dependency chain for quinn-proto (Cargo ecosystem):

The quinn-proto crate is part of the quinn QUIC implementation library. Based on the Cargo ecosystem and the component label `pscomponent:org/rhtpa-server`, the dependency chain is:

```
backend (workspace) -> reqwest/hyper (HTTP client/server) -> quinn -> quinn-proto
Profile: production (quinn-proto is a runtime dependency for QUIC transport)

First appeared: present in all versions (2.1.0 onward)
Fixed in: 2.2.3 (tag v0.4.11 bumped quinn-proto to 0.11.14)
```

quinn-proto is a transitive dependency pulled in through the QUIC protocol stack. It is included in production builds (not dev-only), confirming the vulnerability affects shipped artifacts.

## 2.5 -- Upstream Fix Check

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| 2.1.x | Cargo | `release/0.3.z` | Would check: `git -C /home/dev/repos/rhtpa-backend show release/0.3.z:Cargo.lock \| grep -A2 'quinn-proto'` |
| 2.2.x | Cargo | `release/0.4.z` | Would check: `git -C /home/dev/repos/rhtpa-backend show release/0.4.z:Cargo.lock \| grep -A2 'quinn-proto'` |

Based on the version impact table, versions 2.2.3 and 2.2.4 already ship quinn-proto 0.11.14. This strongly suggests the upstream branch `release/0.4.z` already has the fix. The 2.1.x stream (release/0.3.z) still ships 0.11.9, so the fix status on that branch is uncertain without checking HEAD.

## Cross-Stream Impact Summary

This issue is scoped to stream **2.2.x** (per the `[rhtpa-2.2]` suffix). However, version impact analysis reveals that stream **2.1.x** is also affected:

- 2.1.0: quinn-proto 0.11.9 -- AFFECTED
- 2.1.1: quinn-proto 0.11.9 -- AFFECTED

This triggers **Case B (Cross-stream impact)** in Step 7. The 2.1.x stream versions will be reported as cross-stream impact, and proactive remediation tasks will be created for that stream if no sibling CVE Jira exists for it.
