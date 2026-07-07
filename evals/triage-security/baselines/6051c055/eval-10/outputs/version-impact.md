# Version Impact Analysis — CVE-2026-55123

## Version Impact Table

Version Impact for CVE-2026-55123 (tokio < 1.42.0):

| Version | Stream | tokio version | Affected? | Notes |
|---------|--------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | YES | |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | YES | |

## Cross-Stream Impact Summary

- **Issue scope**: rhtpa-2.2 (from summary suffix [rhtpa-2.2])
- **In-scope versions affected**: RHTPA 2.2.0 (tokio 1.41.1), RHTPA 2.2.1 (tokio 1.41.1)
- **Out-of-scope versions affected**: RHTPA 2.1.0 (tokio 1.40.0), RHTPA 2.1.1 (tokio 1.40.0)
- **Fix threshold**: tokio >= 1.42.0

All versions across both streams ship tokio below the fix threshold of 1.42.0.

Stream rhtpa-2.1 is also affected but falls outside this issue's scope. Cross-stream impact handling (Case B) applies.

## Sibling CVE Jira Search

JQL: `project = TC AND issuetype = 10024 AND labels = "CVE-2026-55123" AND summary ~ "[rhtpa-2.1]"`

**Result**: No sibling Vulnerability issues found for CVE-2026-55123 in stream rhtpa-2.1.

This triggers Case B (preemptive remediation) for stream rhtpa-2.1.

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

| Stream | Ecosystem | Repository | Upstream Branch | Upstream fix PR |
|--------|-----------|------------|-----------------|-----------------|
| 2.1.x | Cargo | backend | release/0.3.z | https://github.com/tokio-rs/tokio/pull/7001 |
| 2.2.x | Cargo | backend | release/0.4.z | https://github.com/tokio-rs/tokio/pull/7001 |
