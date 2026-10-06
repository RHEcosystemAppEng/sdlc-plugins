# Version Impact Analysis -- TC-8004

## Step 2 -- Version Impact Table

CVE-2026-33501 affects h2 versions before 0.4.8 (fixed in 0.4.8).

| Version | Stream | Build Tag | h2 version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | YES | h2 0.4.5 < 0.4.8 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | YES | h2 0.4.5 < 0.4.8 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.4.8 | NO | h2 0.4.8 >= 0.4.8 (fixed version) |
| 2.2.1 | 2.2.x | v0.4.8 | 0.4.8 | NO | h2 0.4.8 >= 0.4.8 |
| 2.2.2 | 2.2.x | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.4.9 | NO | h2 0.4.9 >= 0.4.8 |
| 2.2.4 | 2.2.x | v0.4.12 | 0.4.9 | NO | h2 0.4.9 >= 0.4.8 |

## Stream Impact Summary

| Stream | Affected Versions | Status |
|--------|-------------------|--------|
| 2.1.x | 2.1.0, 2.1.1 | **AFFECTED** -- all versions ship vulnerable h2 0.4.5 |
| 2.2.x | _(none)_ | **NOT AFFECTED** -- all versions ship h2 >= 0.4.8 (patched) |

## Mixed Impact Analysis

This is a **mixed impact** scenario: the 2.1.x stream is fully affected while the
2.2.x stream ships the patched dependency across all its versions. The vulnerability
was resolved in the 2.2.x stream from its first release (2.2.0 ships h2 0.4.8, which
is exactly the fixed version).

## Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> h2
  Type: source dependency (Cargo crate)
  Ecosystem: Cargo
  Lock file: Cargo.lock
  Profile: production (h2 is a runtime dependency)

Remediation: bump h2 to >= 0.4.8 in Cargo.toml / Cargo.lock
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Notes |
|--------|-----------|-----------------|-------|
| 2.1.x | Cargo | release/0.3.z | Upstream fix status must be checked at branch HEAD |
| 2.2.x | Cargo | release/0.4.z | Already ships fixed version -- no remediation needed |

Upstream fix PR: [hyperium/h2#812](https://github.com/hyperium/h2/pull/812)
