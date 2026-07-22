# Version Impact Analysis — CVE-2026-55123 (tokio)

## Version Impact Table

Version Impact for CVE-2026-55123 (tokio < 1.42.0):

| Version | Stream | tokio version | Affected? | Notes |
|---------|--------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | **YES** | Cross-stream (outside issue scope) |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | **YES** | Cross-stream (outside issue scope) |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | **YES** | In-scope stream |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | **YES** | In-scope stream |

Fix threshold: **1.42.0** (from Jira description and external CVE data)

## Cross-Stream Impact Summary

- **Issue scope**: rhtpa-2.2 (stream 2.2.x)
- **In-scope affected versions**: RHTPA 2.2.0, RHTPA 2.2.1 (tokio 1.41.1 < 1.42.0)
- **Cross-stream affected versions**: RHTPA 2.1.0, RHTPA 2.1.1 (tokio 1.40.0 < 1.42.0)

Stream rhtpa-2.1 ships tokio 1.40.0, which is below the fix threshold of 1.42.0. This stream is **affected** but outside the scope of TC-8020. Cross-stream remediation is required (Case B).

## Dependency Chain Context

```
Dependency chain for tokio:
  backend (workspace) -> tokio
  Type: direct dependency
  Profile: production (tokio is a runtime dependency)

Remediation: bump tokio to >= 1.42.0 in Cargo.toml
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | Fix available via upstream PR tokio-rs/tokio#7001 |
| 2.2.x | Cargo | release/0.4.z | Fix available via upstream PR tokio-rs/tokio#7001 |
