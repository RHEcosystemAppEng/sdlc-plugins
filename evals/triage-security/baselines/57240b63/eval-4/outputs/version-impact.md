# Step 2 -- Version Impact Analysis: CVE-2026-33501

## Version Impact Table

CVE-2026-33501 affects h2 versions before 0.4.8. Fix threshold: >= 0.4.8.

| Version | Stream | Build Tag | h2 version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | **YES** | ships vulnerable h2 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | **YES** | ships vulnerable h2 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.4.8 | NO | ships fixed version (= 0.4.8) |
| 2.2.1 | 2.2.x | v0.4.8 | 0.4.8 | NO | ships fixed version |
| 2.2.2 | 2.2.x | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.4.9 | NO | ships version above fix threshold |
| 2.2.4 | 2.2.x | v0.4.12 | 0.4.9 | NO | ships version above fix threshold |

## Stream Impact Summary

| Stream | Affected? | Details |
|--------|-----------|---------|
| 2.1.x | **YES** | All versions (2.1.0, 2.1.1) ship h2 0.4.5 (vulnerable) |
| 2.2.x | NO | All versions ship h2 >= 0.4.8 (at or above fix threshold) |

## Dependency Chain Context (Step 2.3.5)

The h2 crate is a Cargo (Rust) source dependency in the backend repository.

```
Dependency chain for h2:
  backend (workspace) -> hyper -> h2
  Profile: production (hyper is a runtime HTTP dependency)

  Present in: 2.1.x (h2 0.4.5 -- vulnerable)
  Fixed in: 2.2.x (h2 >= 0.4.8 -- at or above fix threshold)
```

The h2 crate is a transitive dependency via hyper (the HTTP library). Remediation
requires bumping h2 (or hyper) in Cargo.lock on the release/0.3.z upstream branch
to bring h2 to >= 0.4.8.

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | h2 at HEAD (latest tag) | Fixed? |
|--------|-----------|-----------------|-------------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.4.5 (at v0.3.12) | **NO** |
| 2.2.x | Cargo | release/0.4.z | 0.4.9 (at v0.4.12) | YES |

The 2.1.x upstream branch (release/0.3.z) has NOT yet picked up the fix -- the
latest tag v0.3.12 still ships h2 0.4.5. Remediation requires an upstream PR to
bump h2 on release/0.3.z, followed by a downstream propagation in the Konflux
release repo.
