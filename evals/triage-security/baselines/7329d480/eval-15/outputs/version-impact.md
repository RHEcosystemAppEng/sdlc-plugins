# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Version Impact Table

Version impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Build Tag | quinn-proto | Affected? | Notes |
|--------|---------|-----------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Summary

- **Affected versions (2.2.x stream -- issue scope):** 2.2.0, 2.2.1, 2.2.2
- **Not affected versions (2.2.x stream):** 2.2.3, 2.2.4 (ship quinn-proto 0.11.14, the fixed version)
- **Cross-stream impact (2.1.x):** 2.1.0, 2.1.1 are both affected (ship quinn-proto 0.11.9)
- **Fix threshold:** quinn-proto >= 0.11.14

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  Ecosystem: Cargo (Rust crate)
  Lock file: Cargo.lock
  Repository: backend

  First affected in 2.2.x: 2.2.0 (tag v0.4.5, quinn-proto 0.11.9)
  Fixed in 2.2.x: 2.2.3 (tag v0.4.11, quinn-proto bumped to 0.11.14)
  
  2.1.x stream: all versions affected (both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9)
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at Tag | Fixed? |
|--------|-----------|-----------------|----------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (at v0.4.11+) | YES |
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (at v0.3.12) | NO |

- **2.2.x stream**: upstream fix is available -- the fix was picked up in build 0.4.11 (version 2.2.3). Remediation for affected versions (2.2.0-2.2.2) involves rebuilding with the updated dependency.
- **2.1.x stream**: upstream branch `release/0.3.z` still ships quinn-proto 0.11.9. An upstream backport is needed before downstream propagation.
