# Step 2 -- Version Impact Analysis: TC-8004

## Version Impact for CVE-2026-33501 (h2 < 0.4.8)

| Version | Stream | Build Tag | h2 version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | YES | ships vulnerable h2 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | YES | ships vulnerable h2 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.4.8 | NO | ships fixed version |
| 2.2.1 | 2.2.x | v0.4.8 | 0.4.8 | NO | ships fixed version |
| 2.2.2 | 2.2.x | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.4.9 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.4.9 | NO | ships fixed version |

## Stream Impact Summary

| Stream | Affected? | Details |
|--------|-----------|---------|
| 2.1.x | YES | All versions (2.1.0, 2.1.1) ship h2 0.4.5, which is below the fix threshold of 0.4.8 |
| 2.2.x | NO | All versions ship h2 >= 0.4.8 (the fixed version or later) |

## Dependency Chain

```
Dependency chain for h2:
  backend (workspace) -> h2
  Type: source dependency (Cargo crate)
  Ecosystem: Cargo
  Lock file: Cargo.lock
  Profile: production (h2 is a runtime HTTP/2 dependency)

  2.1.x stream: h2 0.4.5 (VULNERABLE -- below fix threshold 0.4.8)
  2.2.x stream: h2 0.4.8+ (FIXED -- at or above fix threshold)
```

## Lock File Evidence

Lock file inspection performed via `git show <tag>:Cargo.lock` for each pinned build tag from the supportability matrix:

- `git show v0.3.8:Cargo.lock` -> h2 0.4.5 (2.1.0)
- `git show v0.3.12:Cargo.lock` -> h2 0.4.5 (2.1.1)
- `git show v0.4.5:Cargo.lock` -> h2 0.4.8 (2.2.0)
- `git show v0.4.8:Cargo.lock` -> h2 0.4.8 (2.2.1)
- v0.4.9: retag of v0.4.8, skipped (same as 2.2.1)
- `git show v0.4.11:Cargo.lock` -> h2 0.4.9 (2.2.3)
- `git show v0.4.12:Cargo.lock` -> h2 0.4.9 (2.2.4)

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix Status |
|--------|-----------|-----------------|------------|
| 2.1.x | Cargo | release/0.3.z | Needs upstream backport -- h2 0.4.5 on branch, fix threshold is 0.4.8 |
| 2.2.x | Cargo | release/0.4.z | Already fixed -- h2 >= 0.4.8 on branch |
