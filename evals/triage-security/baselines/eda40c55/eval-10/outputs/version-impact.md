# Version Impact Analysis — TC-8020

## Version Impact for CVE-2026-55123 (tokio < 1.42.0)

| Version | Stream | tokio version | Affected? | Notes |
|---------|--------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 (2.1.x) | 1.40.0 | YES | |
| RHTPA 2.1.1 | rhtpa-2.1 (2.1.x) | 1.40.0 | YES | |
| RHTPA 2.2.0 | rhtpa-2.2 (2.2.x) | 1.41.1 | YES | |
| RHTPA 2.2.1 | rhtpa-2.2 (2.2.x) | 1.41.1 | YES | |

Fix threshold: **1.42.0** (versions before 1.42.0 are vulnerable)

## Cross-Stream Impact Summary

- **Stream rhtpa-2.2 (2.2.x)**: AFFECTED -- tokio 1.41.1 < 1.42.0 (this is the current issue's stream)
- **Stream rhtpa-2.1 (2.1.x)**: AFFECTED -- tokio 1.40.0 < 1.42.0 (cross-stream impact)

## Sibling CVE Jira Search

JQL search for sibling CVE Jiras with label `CVE-2026-55123`:

- **Stream rhtpa-2.2**: TC-8020 (current issue) -- exists
- **Stream rhtpa-2.1**: **No CVE Jira exists** -- no sibling Vulnerability issue found

This triggers Case B (preemptive remediation) for stream rhtpa-2.1.

## Dependency Chain Context

```
Dependency chain for tokio:
  backend (workspace) -> tokio (direct or transitive dependency)
  Ecosystem: Cargo
  Profile: production (tokio is a runtime dependency)

  Stream 2.1.x: tokio 1.40.0 (all versions)
  Stream 2.2.x: tokio 1.41.1 (all versions)
  Fix threshold: 1.42.0
```
