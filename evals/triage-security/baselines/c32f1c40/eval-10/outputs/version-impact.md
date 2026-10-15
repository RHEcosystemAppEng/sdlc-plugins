# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-55123 (tokio < 1.42.0)

### 2.2.x stream (current issue scope: rhtpa-2.2)

| Version | Build Tag | tokio version | Affected? | Notes |
|---------|-----------|---------------|-----------|-------|
| RHTPA 2.2.0 | v0.4.5 | 1.41.1 | YES | tokio 1.41.1 < 1.42.0 |
| RHTPA 2.2.1 | v0.4.8 | 1.41.1 | YES | tokio 1.41.1 < 1.42.0 |
| RHTPA 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as RHTPA 2.2.1) |
| RHTPA 2.2.3 | v0.4.11 | 1.42.0 | NO | tokio 1.42.0 >= 1.42.0 (fixed) |
| RHTPA 2.2.4 | v0.4.12 | 1.42.0 | NO | tokio 1.42.0 >= 1.42.0 (fixed) |

### 2.1.x stream (cross-stream analysis)

| Version | Build Tag | tokio version | Affected? | Notes |
|---------|-----------|---------------|-----------|-------|
| RHTPA 2.1.0 | v0.3.8 | 1.40.0 | YES | tokio 1.40.0 < 1.42.0 |
| RHTPA 2.1.1 | v0.3.12 | 1.40.0 | YES | tokio 1.40.0 < 1.42.0 |

## Cross-Stream Impact Summary

- **2.2.x stream**: versions 2.2.0, 2.2.1, and 2.2.2 are affected; versions 2.2.3 and 2.2.4 ship the fixed version
- **2.1.x stream**: ALL versions (2.1.0 and 2.1.1) are affected -- tokio 1.40.0 is well below the fix threshold of 1.42.0

Stream rhtpa-2.1 is also affected but is outside the current issue's scope ([rhtpa-2.2]). A JQL search for sibling CVE Jiras with label CVE-2026-55123 in stream rhtpa-2.1 returns **no results** -- no CVE Jira exists for that stream. This triggers Case A (cross-stream proactive remediation) in Step 8.

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for tokio:
  rhtpa-server (workspace) -> tokio
  Type: direct dependency
  Profile: production (tokio is a runtime async dependency)

Remediation: bump tokio to >= 1.42.0 in Cargo.toml
```

tokio is a direct production dependency of the rhtpa-server workspace. It is present in all supported versions across both streams. Remediation is a straightforward version bump in Cargo.toml/Cargo.lock.

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Upstream Fix PR | Fix Available? |
|--------|-----------|-----------------|-----------------|----------------|
| 2.2.x | Cargo | release/0.4.z | tokio-rs/tokio#7001 | To be verified via `git show release/0.4.z:Cargo.lock` |
| 2.1.x | Cargo | release/0.3.z | tokio-rs/tokio#7001 | To be verified via `git show release/0.3.z:Cargo.lock` |
