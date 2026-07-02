# Version Impact Analysis — CVE-2026-55123 (tokio < 1.42.0)

## Version Impact Table

| Version | Stream | tokio version | Affected? | Notes |
|---------|--------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | YES | |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | YES | |

## Cross-Stream Impact Summary

- **Issue stream scope**: rhtpa-2.2 (2.2.x)
- **Scoped affected versions**: RHTPA 2.2.0, RHTPA 2.2.1 (tokio 1.41.1, threshold 1.42.0)
- **Cross-stream affected versions**: RHTPA 2.1.0, RHTPA 2.1.1 (tokio 1.40.0, threshold 1.42.0)

All versions across both streams ship tokio < 1.42.0 and are affected.

Stream rhtpa-2.1 is also affected but is outside this issue's scope. The cross-stream
impact triggers Case B (proactive preemptive remediation) since no sibling CVE Jira
exists for stream rhtpa-2.1.

## Sibling CVE Jira Search

JQL: `project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020`

**Result**: No sibling Vulnerability issues found for CVE-2026-55123 in stream rhtpa-2.1.

## Ecosystem Mappings (from security-matrix.md)

### Stream 2.1.x (rhtpa-release.0.3.z)

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
