# Step 2 -- Version Impact Analysis: CVE-2026-55123

## Version Impact Table

Version Impact for CVE-2026-55123 (tokio < 1.42.0):

| Version | Stream | tokio version | Affected? | Notes |
|---------|--------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | YES | |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | YES | |

Fix threshold: **1.42.0** (from Jira description, cross-validated against external CVE databases)

All versions across both streams ship tokio < 1.42.0 and are therefore affected.

## Cross-Stream Impact Summary

- **Issue stream scope**: rhtpa-2.2 (2.2.x)
- **In-scope versions affected**: RHTPA 2.2.0 (tokio 1.41.1), RHTPA 2.2.1 (tokio 1.41.1)
- **Out-of-scope streams affected**: rhtpa-2.1 (2.1.x)
  - RHTPA 2.1.0: tokio 1.40.0 -- **AFFECTED**
  - RHTPA 2.1.1: tokio 1.40.0 -- **AFFECTED**

## Dependency Chain Context

```
Dependency chain for tokio:
  backend (workspace) -> tokio
  Type: direct dependency
  Profile: production (tokio is a runtime dependency)
  Ecosystem: Cargo

Remediation: bump tokio to >= 1.42.0 in Cargo.toml
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Source Repo | Notes |
|--------|-----------|-----------------|-------------|-------|
| 2.1.x | Cargo | release/0.3.z | backend | Upstream fix available via [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) |
| 2.2.x | Cargo | release/0.4.z | backend | Upstream fix available via [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) |

## Sibling CVE Jira Search

JQL: `project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020`

**Result**: No sibling Vulnerability issues found for CVE-2026-55123 in stream rhtpa-2.1.

This means stream rhtpa-2.1 has no dedicated CVE Jira -- preemptive remediation tasks are required (Case A).
