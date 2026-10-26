# Version Impact Analysis -- Step 2

## Version Impact for CVE-2026-55123 (tokio < 1.42.0)

Fix threshold: **1.42.0** (from Jira description; cross-validated with external CVE data)

| Version | Stream | tokio version | Affected? | Notes |
|---------|--------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | YES | |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | YES | |

All supported versions across both streams ship tokio < 1.42.0 and are affected.

## Cross-Stream Summary

- **rhtpa-2.2 (current issue scope)**: RHTPA 2.2.0 and 2.2.1 are affected (tokio 1.41.1 < 1.42.0)
- **rhtpa-2.1 (other stream)**: RHTPA 2.1.0 and 2.1.1 are affected (tokio 1.40.0 < 1.42.0)

## Dependency Chain Context

```
Dependency chain for tokio:
  backend (workspace) -> tokio
  Type: direct dependency (assumed based on tokio being a core async runtime)
  Profile: production (tokio is a runtime dependency)
  Ecosystem: Cargo
  Lock file: Cargo.lock
```

## Ecosystem Mappings (from security-matrix.md)

### Stream rhtpa-2.1 (rhtpa-release.0.3.z)

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |

### Stream rhtpa-2.2 (rhtpa-release.0.4.z)

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

## Affects Versions Correction (Step 3)

- Issue is scoped to stream **rhtpa-2.2**
- PSIRT-assigned Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1
- Lock file evidence confirms: RHTPA 2.2.0 (tokio 1.41.1, affected) and RHTPA 2.2.1 (tokio 1.41.1, affected)
- **Affects Versions are correct** -- no correction needed for the scoped stream

## Sibling / Duplicate Check (Step 4)

- JQL search for label `CVE-2026-55123` in project TC (excluding TC-8020): **no sibling Vulnerability issues found**
- No same-stream duplicates
- No cross-stream companion CVE Jiras exist for rhtpa-2.1

## Cross-Stream Impact Detection

Since the issue is scoped to rhtpa-2.2 and rhtpa-2.1 is also affected but has **no CVE Jira**, this triggers **Case A: Cross-stream impact with proactive remediation**.
