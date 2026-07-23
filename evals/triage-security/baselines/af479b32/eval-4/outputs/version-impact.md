# Version Impact Analysis — CVE-2026-33501

## Version Impact Table

Version Impact for CVE-2026-33501 (h2 < 0.4.8):

| Version | Stream | Build Tag | h2 version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0   | 2.1.x  | v0.3.8    | 0.4.5      | YES       |       |
| 2.1.1   | 2.1.x  | v0.3.12   | 0.4.5      | YES       |       |
| 2.2.0   | 2.2.x  | v0.4.5    | 0.4.8      | NO        | ships fixed version |
| 2.2.1   | 2.2.x  | v0.4.8    | 0.4.8      | NO        | ships fixed version |
| 2.2.2   | 2.2.x  | v0.4.9    | --         | NO        | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3   | 2.2.x  | v0.4.11   | 0.4.9      | NO        | ships version above fix threshold |
| 2.2.4   | 2.2.x  | v0.4.12   | 0.4.9      | NO        | ships version above fix threshold |

## Stream Impact Summary

| Stream | Affected Versions | Unaffected Versions | Status |
|--------|-------------------|---------------------|--------|
| 2.1.x  | 2.1.0, 2.1.1      | _(none)_            | AFFECTED -- all versions in this stream ship h2 0.4.5 (vulnerable) |
| 2.2.x  | _(none)_           | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 | NOT AFFECTED -- all versions ship h2 >= 0.4.8 (fixed) |

## Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> h2
  Type: source dependency (Cargo crate)
  Ecosystem: Cargo
  Lock file: Cargo.lock

  Stream 2.1.x:
    v0.3.8  (2.1.0): h2 0.4.5 — AFFECTED (< 0.4.8)
    v0.3.12 (2.1.1): h2 0.4.5 — AFFECTED (< 0.4.8)

  Stream 2.2.x:
    v0.4.5  (2.2.0): h2 0.4.8 — NOT AFFECTED (= 0.4.8, fix threshold)
    v0.4.8  (2.2.1): h2 0.4.8 — NOT AFFECTED
    v0.4.9  (2.2.2): retag of v0.4.8 — NOT AFFECTED (same as 2.2.1)
    v0.4.11 (2.2.3): h2 0.4.9 — NOT AFFECTED (> 0.4.8)
    v0.4.12 (2.2.4): h2 0.4.9 — NOT AFFECTED (> 0.4.8)
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | h2 version at branch tag | Fixed? |
|--------|-----------|-----------------|--------------------------|--------|
| 2.1.x  | Cargo     | release/0.3.z   | 0.4.5 (at v0.3.12)      | NO     |
| 2.2.x  | Cargo     | release/0.4.z   | 0.4.8+ (at v0.4.5+)     | YES    |

The 2.1.x stream's upstream branch (`release/0.3.z`) does NOT yet include the h2 fix. Remediation requires an upstream PR to bump h2 to >= 0.4.8 on `release/0.3.z`, followed by a downstream propagation in the Konflux release repo.

The 2.2.x stream already ships h2 >= 0.4.8 across all versions -- no remediation needed.
