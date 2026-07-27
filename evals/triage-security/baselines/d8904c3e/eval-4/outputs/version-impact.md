# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-33501 (h2 < 0.4.8)

| Version | Stream | Build Tag | h2 version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | YES | < 0.4.8 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | YES | < 0.4.8 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.4.8 | NO | >= 0.4.8 (fixed) |
| 2.2.1 | 2.2.x | v0.4.8 | 0.4.8 | NO | >= 0.4.8 (fixed) |
| 2.2.2 | 2.2.x | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.4.9 | NO | >= 0.4.8 (fixed) |
| 2.2.4 | 2.2.x | v0.4.12 | 0.4.9 | NO | >= 0.4.8 (fixed) |

## Stream Impact Summary

| Stream | Affected Versions | Unaffected Versions | Stream Status |
|--------|-------------------|---------------------|---------------|
| 2.1.x | 2.1.0, 2.1.1 | _(none)_ | AFFECTED -- all versions ship vulnerable h2 |
| 2.2.x | _(none)_ | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 | NOT AFFECTED -- all versions ship fixed h2 |

## Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> h2
  Type: direct dependency (Cargo ecosystem)
  Profile: production (h2 is a runtime dependency)

  Stream 2.1.x: h2 0.4.5 at tags v0.3.8 and v0.3.12
  Stream 2.2.x: h2 >= 0.4.8 at all tags (v0.4.5 onward)

Remediation: bump h2 to >= 0.4.8 in Cargo.toml on release/0.3.z branch
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | h2 at HEAD (inferred) | Fixed? |
|--------|-----------|-----------------|------------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.4.5 (last shipped) | NO -- upstream branch still ships 0.4.5 |
| 2.2.x | Cargo | release/0.4.z | 0.4.9 (last shipped) | YES -- already >= 0.4.8 |

The 2.1.x upstream branch (release/0.3.z) requires an upstream backport PR to bump
h2 to >= 0.4.8 before the downstream Konflux release repo can pick up the fix.
