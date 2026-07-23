# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Version Impact Table

Version impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | `v0.4.9` | 0.11.12 | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | ships fixed version |

### Lock File Evidence

Each quinn-proto version was extracted via `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'` using the pinned backend commit from the supportability matrix.

- Versions 2.2.3+ ship quinn-proto 0.11.14, which is the fixed version -- NOT affected.
- Versions 2.2.0-2.2.2 ship quinn-proto < 0.11.14 -- AFFECTED.
- All 2.1.x versions ship quinn-proto 0.11.9 -- AFFECTED.

### Retag Handling

Version 2.2.2 (build 0.4.9) is a retag of 2.2.1 (build 0.4.8) -- the backend source commit is identical (`v0.4.8`). The lock file check was skipped and the result carried forward from 2.2.1.

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (present in Cargo.lock at workspace level)
  Profile: production (quinn-proto is a runtime dependency for QUIC transport)

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml / Cargo.lock
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | (needs verification) | Unknown |
| 2.2.x | Cargo | release/0.4.z | (needs verification) | Unknown |

Note: In a live triage, `git show release/0.4.z:Cargo.lock` and `git show release/0.3.z:Cargo.lock` would be run against the rhtpa-backend repo to determine upstream fix status. Since the supportability matrix shows that build 0.4.11 (used by 2.2.3) already ships 0.11.14, the upstream fix is likely already on `release/0.4.z`.

## Affects Versions Correction (Step 3)

The issue is scoped to stream **2.2.x**. Only 2.2.x versions are included in the correction.

- **Current (PSIRT-assigned)**: `[RHTPA 2.0.0]`
- **Proposed**: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

RHTPA 2.0.0 does not correspond to any configured version stream. The correction replaces it with the 2.2.x versions that are actually affected based on lock file evidence.

Versions 2.2.3 and 2.2.4 are excluded because they ship quinn-proto 0.11.14 (the fixed version).

## Cross-Stream Impact Summary

The issue is scoped to 2.2.x, but stream **2.1.x** is also affected:

- 2.1.0: quinn-proto 0.11.9 -- AFFECTED
- 2.1.1: quinn-proto 0.11.9 -- AFFECTED

This triggers **Case B** (cross-stream impact) in Step 8. Preemptive remediation tasks will be created for stream 2.1.x unless a sibling CVE Jira already exists for that stream.
