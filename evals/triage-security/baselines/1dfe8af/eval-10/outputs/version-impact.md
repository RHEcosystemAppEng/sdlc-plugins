# Version Impact Analysis — TC-8020

## Version Impact for CVE-2026-55123 (tokio < 1.42.0)

Fix threshold: 1.42.0 (versions before 1.42.0 are vulnerable)

| Version | Stream | tokio version | Affected? | Notes |
|---------|--------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | YES | |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | YES | |

## Cross-Stream Impact Summary

- **Issue stream scope**: rhtpa-2.2 (2.2.x)
- **Versions within scope (rhtpa-2.2)**: RHTPA 2.2.0 (YES), RHTPA 2.2.1 (YES)
- **Versions outside scope (rhtpa-2.1)**: RHTPA 2.1.0 (YES), RHTPA 2.1.1 (YES)

Stream rhtpa-2.1 is also affected: tokio 1.40.0 is below the fix threshold of 1.42.0.

## Ecosystem Mappings

### Stream 2.1.x (rhtpa-release.0.3.z)

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

## Sibling CVE Jira Search

JQL: `project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020`

**Result**: No sibling Vulnerability issues found for CVE-2026-55123 in stream rhtpa-2.1. No CVE Jira exists for the rhtpa-2.1 stream.

This triggers Case B (cross-stream proactive remediation) for stream rhtpa-2.1.
