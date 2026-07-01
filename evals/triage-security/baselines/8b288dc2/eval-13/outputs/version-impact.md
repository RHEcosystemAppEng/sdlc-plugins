# Step 2 -- Version Impact Analysis for CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | Outside issue scope (cross-stream) |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | Outside issue scope (cross-stream) |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | Fixed: ships >= 0.11.14 |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | Fixed: ships >= 0.11.14 |

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn -> quinn-proto
  Ecosystem: Cargo (Rust crate)
  Lock file: Cargo.lock

  Affected versions: 2.2.0 (0.11.9), 2.2.1 (0.11.12), 2.2.2 (retag of 2.2.1)
  Fixed in: 2.2.3+ (0.11.14)
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Repository | Version at HEAD | Fixed? |
|--------|-----------|-----------------|------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | backend | 0.11.14 | YES |
| 2.1.x | Cargo | release/0.3.z | backend | 0.11.9 | NO |

## Cross-Stream Impact Summary

- **2.2.x** (issue scope): versions 2.2.0, 2.2.1, 2.2.2 are affected. Versions 2.2.3, 2.2.4 are NOT affected.
- **2.1.x** (cross-stream): versions 2.1.0, 2.1.1 are affected. Upstream branch `release/0.3.z` is NOT fixed.
- The 2.1.x stream is outside this issue's scope and would be handled by Case B (cross-stream impact comment).
