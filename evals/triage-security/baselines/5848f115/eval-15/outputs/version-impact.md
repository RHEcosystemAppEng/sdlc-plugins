# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | fixed version shipped |
| 2.2.4 | 2.2.x | 0.11.14 | NO | fixed version shipped |

## Summary

- **Scoped stream (2.2.x)**: versions 2.2.0, 2.2.1, 2.2.2 are affected; versions 2.2.3 and 2.2.4 ship the fix (quinn-proto 0.11.14)
- **Cross-stream (2.1.x)**: versions 2.1.0, 2.1.1 are affected (quinn-proto 0.11.9, both pinned at v0.3.8 and v0.3.12 respectively)
- Fix threshold: quinn-proto >= 0.11.14

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: source dependency (Cargo crate)
  Ecosystem: Cargo
  Lock file: Cargo.lock
  Profile: production (runtime dependency)

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml / Cargo.lock
Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at Tag | Fixed? |
|--------|-----------|-----------------|----------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (at v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (at v0.4.11+) | YES |

The 2.2.x stream already has the fix in later releases (v0.4.11+, shipping quinn-proto 0.11.14). The 2.1.x stream does not have the fix at the latest pinned tag (v0.3.12, shipping quinn-proto 0.11.9).
