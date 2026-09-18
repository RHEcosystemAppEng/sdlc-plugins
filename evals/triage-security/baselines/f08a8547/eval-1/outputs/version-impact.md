# Step 2 -- Version Impact Analysis

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | `v0.4.9` | 0.11.12 | YES | retag of 2.2.1 (same backend commit as v0.4.8) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | |

Fix threshold: >= 0.11.14 (from CVE description, confirmed by advisory GHSA-2026-qp73-x4mq).

## Dependency Chain Context

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) -> quinn-proto
  Type: direct dependency
  Profile: production (quinn-proto is a runtime dependency for QUIC transport)
  
  Present in all versions across both streams (2.1.x and 2.2.x).
  
Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml / Cargo.lock
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix Status | Notes |
|--------|-----------|-----------------|------------|-------|
| 2.1.x | Cargo | release/0.3.z | Needs verification | Check `git show release/0.3.z:Cargo.lock` at branch HEAD |
| 2.2.x | Cargo | release/0.4.z | YES | v0.4.11+ already ships quinn-proto 0.11.14 |

Stream 2.2.x: The upstream fix is already present on release/0.4.z -- versions
2.2.3 (v0.4.11) and 2.2.4 (v0.4.12) ship the fixed quinn-proto 0.11.14.
Remediation for this stream requires downstream propagation only (the fix
has already landed upstream).

Stream 2.1.x: The latest released version (2.1.1, tag v0.3.12) ships
quinn-proto 0.11.9. Upstream branch HEAD on release/0.3.z must be checked
to determine if the fix has been backported.
