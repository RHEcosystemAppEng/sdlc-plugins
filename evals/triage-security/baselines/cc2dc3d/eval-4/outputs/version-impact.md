# Step 2 -- Version Impact Analysis: CVE-2026-33501

## Version Impact Table

Version Impact for CVE-2026-33501 (h2 versions before 0.4.8):

| Version | Stream | Build Tag | h2 version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | YES | < 0.4.8 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | YES | < 0.4.8 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.4.8 | NO | = 0.4.8 (fixed version) |
| 2.2.1 | 2.2.x | v0.4.8 | 0.4.8 | NO | = 0.4.8 (fixed version) |
| 2.2.2 | 2.2.x | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.4.9 | NO | > 0.4.8 |
| 2.2.4 | 2.2.x | v0.4.12 | 0.4.9 | NO | > 0.4.8 |

## Impact Summary

- **2.1.x stream**: ALL versions affected (2.1.0, 2.1.1 both ship h2 0.4.5)
- **2.2.x stream**: NO versions affected (all versions ship h2 >= 0.4.8)

This is a **mixed impact** scenario -- the vulnerability affects the 2.1.x stream but has already been resolved in the 2.2.x stream. The 2.2.x stream picked up the fix starting from version 2.2.0 (build tag v0.4.5), which ships h2 0.4.8 (the exact fixed version).

## Dependency Chain Context (Step 2.3.5)

For the affected 2.1.x versions, the h2 dependency enters the build through the backend source repository:

```
Dependency chain for h2:
  backend (workspace) -> hyper -> h2
  Ecosystem: Cargo (Cargo.lock)
  Profile: production (hyper is a runtime HTTP/2 dependency)

Present in: 2.1.x (h2 0.4.5 -- vulnerable)
Fixed in: 2.2.x (h2 >= 0.4.8 -- patched)
```

The h2 crate is a transitive dependency pulled in via hyper (the HTTP library). It is a production dependency -- not dev-only or build-only -- so all product versions shipping this version are genuinely exposed.

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | Needs verification -- check if h2 >= 0.4.8 at branch HEAD |
| 2.2.x | Cargo | release/0.4.z | Already fixed -- all released versions ship h2 >= 0.4.8 |

The upstream fix PR is [hyperium/h2#812](https://github.com/hyperium/h2/pull/812). The 2.2.x stream already ships the fixed version. For the 2.1.x stream, remediation requires bumping h2 to >= 0.4.8 on the `release/0.3.z` branch of the backend repository.
