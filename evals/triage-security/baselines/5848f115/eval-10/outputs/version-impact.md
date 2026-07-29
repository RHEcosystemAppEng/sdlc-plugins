# Version Impact Analysis -- CVE-2026-55123

## Version Impact Table

Version impact for CVE-2026-55123 (tokio < 1.42.0, fixed in 1.42.0):

| Version | Stream | tokio version | Affected? | Notes |
|---------|--------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | YES | |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | YES | |

All versions across both streams ship tokio < 1.42.0 and are affected by CVE-2026-55123.

### Stream-Scoped View

**Issue stream (rhtpa-2.2):**

| Version | tokio version | Affected? |
|---------|---------------|-----------|
| RHTPA 2.2.0 | 1.41.1 | YES |
| RHTPA 2.2.1 | 1.41.1 | YES |

**Other streams (cross-stream impact):**

| Version | Stream | tokio version | Affected? |
|---------|--------|---------------|-----------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | YES |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | YES |

### Dependency Chain Context

```
Dependency chain for tokio:
  backend (workspace) -> tokio
  Type: direct dependency
  Profile: production (tokio is a runtime dependency)

Remediation: bump tokio to >= 1.42.0 in Cargo.toml
```

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Source Repo |
|--------|-----------|-----------------|------------|
| 2.1.x | Cargo | release/0.3.z | rhtpa-backend |
| 2.2.x | Cargo | release/0.4.z | rhtpa-backend |

Upstream fix PR: [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001)

## Cross-Stream Impact Summary

The issue is scoped to stream **rhtpa-2.2**, but version impact analysis reveals
that stream **rhtpa-2.1** is also affected:

- Stream rhtpa-2.1: tokio 1.40.0 (threshold 1.42.0) -- **AFFECTED**
- Stream rhtpa-2.2: tokio 1.41.1 (threshold 1.42.0) -- **AFFECTED** (issue scope)

### Sibling CVE Jira Search (Step 4)

JQL: `project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020`

**Result for stream rhtpa-2.1**: No sibling Vulnerability issues found.

No CVE Jira exists for stream rhtpa-2.1. This triggers Case A preemptive remediation
task creation for that stream.
