# Version Impact Analysis -- Step 2

## Version Impact Table

Version Impact for CVE-2026-55123 (tokio < 1.42.0):

| Version | Stream | tokio version | Affected? | Notes |
|---------|--------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | YES | |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | YES | |

**Fix threshold**: 1.42.0 (from Jira description; external CVE enrichment would cross-validate via MITRE/OSV).

All supported versions across both streams ship tokio below the fix threshold of 1.42.0 and are therefore affected.

## Cross-Stream Impact Summary

This issue is scoped to stream `rhtpa-2.2`. However, the version impact analysis reveals that stream `rhtpa-2.1` is also affected:

- **rhtpa-2.2** (issue scope): RHTPA 2.2.0 and 2.2.1 ship tokio 1.41.1 -- AFFECTED
- **rhtpa-2.1** (cross-stream): RHTPA 2.1.0 and 2.1.1 ship tokio 1.40.0 -- AFFECTED

## Stream-Scoped Impact (for Affects Versions correction)

Since TC-8020 is scoped to stream rhtpa-2.2, only rhtpa-2.2 versions are in scope for this issue's Affects Versions:

| Version | Affected? |
|---------|-----------|
| RHTPA 2.2.0 | YES |
| RHTPA 2.2.1 | YES |

PSIRT-assigned Affects Versions (RHTPA 2.2.0, RHTPA 2.2.1) are **correct** for this stream-scoped issue. No correction needed.

## Source Evidence

### Stream rhtpa-2.1 (2.1.x)

| Version | Build Tag | tokio version | Source |
|---------|-----------|---------------|--------|
| RHTPA 2.1.0 | v0.3.8 | 1.40.0 | `git show v0.3.8:Cargo.lock` |
| RHTPA 2.1.1 | v0.3.12 | 1.40.0 | `git show v0.3.12:Cargo.lock` |

### Stream rhtpa-2.2 (2.2.x)

| Version | Build Tag | tokio version | Source |
|---------|-----------|---------------|--------|
| RHTPA 2.2.0 | v0.4.5 | 1.41.1 | `git show v0.4.5:Cargo.lock` |
| RHTPA 2.2.1 | v0.4.8 | 1.41.1 | `git show v0.4.8:Cargo.lock` |

## Sibling CVE Jiras (Step 4 JQL Search)

JQL: `project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020`

**No sibling Vulnerability issues found** for CVE-2026-55123 in stream rhtpa-2.1.

This means Case A (cross-stream impact with preemptive remediation) applies: stream rhtpa-2.1 is affected but has no CVE Jira, so preemptive remediation tasks must be created for it.
