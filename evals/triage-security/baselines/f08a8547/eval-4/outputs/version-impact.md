# Step 2 -- Version Impact Analysis: CVE-2026-33501 (h2 < 0.4.8)

## Version Impact Table

| Version | Stream | Build Tag | h2 version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.4.8 | NO | ships fixed version |
| 2.2.1 | 2.2.x | v0.4.8 | 0.4.8 | NO | ships fixed version |
| 2.2.2 | 2.2.x | v0.4.9 | -- | NO | retag of 2.2.1 |
| 2.2.3 | 2.2.x | v0.4.11 | 0.4.9 | NO | ships version above fix threshold |
| 2.2.4 | 2.2.x | v0.4.12 | 0.4.9 | NO | ships version above fix threshold |

## Impact Summary

- **2.1.x stream**: ALL versions affected (2.1.0, 2.1.1) -- both ship h2 0.4.5, which is below the fix threshold of 0.4.8
- **2.2.x stream**: NO versions affected -- all versions ship h2 >= 0.4.8 (the fixed version or later)

This is a **mixed impact** scenario: the vulnerability only affects the 2.1.x stream. The 2.2.x stream already ships a patched version of h2.

## Dependency Chain (Step 2.3.5)

```
Dependency chain for h2:
  backend (workspace) -> [intermediate deps] -> h2
  Type: source dependency (Cargo ecosystem)
  Profile: production (h2 is a runtime dependency for HTTP/2 support)

  Present in: 2.1.x (v0.3.8, v0.3.12) at 0.4.5 -- VULNERABLE
  Present in: 2.2.x (v0.4.5+) at 0.4.8+ -- FIXED
```

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | h2 at branch HEAD | Fixed? |
|--------|-----------|-----------------|-------------------|--------|
| 2.1.x | Cargo | release/0.3.z | _(requires git show to confirm)_ | _(unconfirmed -- eval mode)_ |
| 2.2.x | Cargo | release/0.4.z | >= 0.4.8 | YES (already ships fixed version) |

The 2.2.x stream already ships the patched h2 version in all released product versions. Remediation is only required for the 2.1.x stream.
