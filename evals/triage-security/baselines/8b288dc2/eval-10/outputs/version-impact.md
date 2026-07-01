# Version Impact Analysis — CVE-2026-55123

## Version Impact for CVE-2026-55123 (tokio < 1.42.0)

Fix threshold: **1.42.0** (from Jira description, cross-validated with external CVE data)

| Version | Stream | tokio version | Affected? | Notes |
|---------|--------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | YES | |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | YES | |

## Cross-Stream Impact Summary

- **rhtpa-2.2** (issue stream scope): ALL versions affected (2.2.0, 2.2.1 ship tokio 1.41.1)
- **rhtpa-2.1** (other stream): ALL versions affected (2.1.0, 2.1.1 ship tokio 1.40.0)

Both streams ship tokio versions below the fix threshold of 1.42.0.

## Dependency Chain Context

```
Dependency chain for tokio (Cargo):
  Ecosystem: Cargo (Rust crate)
  Lock file: Cargo.lock
  Repository: backend (rhtpa-backend)

  rhtpa-2.2 stream: tokio 1.41.1 at tags v0.4.5, v0.4.8
  rhtpa-2.1 stream: tokio 1.40.0 at tags v0.3.8, v0.3.12

  Profile: production (tokio is a runtime dependency)
```

## Stream-Scoped Impact (for this issue: rhtpa-2.2)

This issue is scoped to stream rhtpa-2.2. Within that stream:

| Version | tokio version | Affected? |
|---------|---------------|-----------|
| RHTPA 2.2.0 | 1.41.1 | YES |
| RHTPA 2.2.1 | 1.41.1 | YES |

Both versions in the scoped stream are affected and require remediation.

## Other Streams Affected (outside issue scope)

Stream rhtpa-2.1 is also affected (tokio 1.40.0 < 1.42.0 fix threshold).
A JQL search for sibling CVE Jiras with label CVE-2026-55123 returns **no results** for stream rhtpa-2.1 -- no CVE Jira exists for that stream.

This triggers **Case B: Cross-stream impact with preemptive remediation** for stream rhtpa-2.1.
