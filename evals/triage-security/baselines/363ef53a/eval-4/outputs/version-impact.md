# Version Impact Analysis — TC-8004

## Version Impact for CVE-2026-33501 (h2 < 0.4.8)

| Version | Stream | Source Tag | h2 version | Affected? | Notes |
|---------|--------|------------|------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.4.5 | YES | h2 0.4.5 < 0.4.8 |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.4.5 | YES | h2 0.4.5 < 0.4.8 |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.4.8 | NO | h2 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.4.8 | NO | h2 0.4.8 >= 0.4.8 |
| 2.2.2 | 2.2.x | `v0.4.9` | — | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.4.9 | NO | h2 0.4.9 >= 0.4.8 |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.4.9 | NO | h2 0.4.9 >= 0.4.8 |

## Stream Impact Summary

| Stream | Affected? | Affected Versions | Shipped h2 Version |
|--------|-----------|-------------------|--------------------|
| 2.1.x | YES | 2.1.0, 2.1.1 | 0.4.5 (all versions) |
| 2.2.x | NO | _(none)_ | 0.4.8+ (all versions at or above fix threshold) |

**Mixed impact**: The 2.1.x stream ships h2 0.4.5 which is vulnerable (below 0.4.8 fix threshold). The 2.2.x stream ships h2 0.4.8 or later which is at or above the fix threshold and is therefore NOT affected.

## Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> h2
  Type: source dependency (Cargo)
  Ecosystem: Cargo
  Lock file: Cargo.lock
  Profile: production (h2 is a runtime HTTP/2 dependency)
```

The h2 crate is used for HTTP/2 protocol handling. It is a production dependency shipped in the container image.

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Latest Tag h2 Version | Fixed? |
|--------|-----------|-----------------|------------------------|--------|
| 2.1.x | Cargo | `release/0.3.z` | 0.4.5 (at v0.3.12) | NO |
| 2.2.x | Cargo | `release/0.4.z` | 0.4.8+ (at v0.4.5+) | YES (not affected) |

The 2.1.x stream's upstream branch (`release/0.3.z`) ships h2 0.4.5 at the latest known tag (v0.3.12), which is below the fix threshold. The upstream fix is NOT yet available on this branch. Remediation requires an upstream backport to bump h2 to >= 0.4.8 on `release/0.3.z`, followed by downstream propagation.

The 2.2.x stream is not affected and requires no remediation.
