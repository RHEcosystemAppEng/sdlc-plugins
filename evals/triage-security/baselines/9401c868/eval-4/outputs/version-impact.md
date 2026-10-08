# Step 2 -- Version Impact Analysis: TC-8004

## Version Impact for CVE-2026-33501 (h2 < 0.4.8)

| Version | Stream | Build Tag | h2 version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | YES | ships vulnerable h2 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | YES | ships vulnerable h2 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.4.8 | NO | ships fixed version (0.4.8) |
| 2.2.1 | 2.2.x | v0.4.8 | 0.4.8 | NO | ships fixed version (0.4.8) |
| 2.2.2 | 2.2.x | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.4.9 | NO | ships version above fix threshold |
| 2.2.4 | 2.2.x | v0.4.12 | 0.4.9 | NO | ships version above fix threshold |

## Stream Impact Summary

| Stream | Affected? | Affected Versions | Unaffected Versions |
|--------|-----------|-------------------|---------------------|
| 2.1.x | YES | 2.1.0, 2.1.1 | _(none)_ |
| 2.2.x | NO | _(none)_ | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 |

**Mixed impact across streams**: The 2.1.x stream ships h2 0.4.5 (vulnerable) in all versions, while the 2.2.x stream ships h2 >= 0.4.8 (fixed) in all versions.

## Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> h2
  Type: direct or transitive dependency (Cargo ecosystem)
  Profile: production (h2 is a runtime HTTP/2 protocol dependency)

  2.1.x stream: h2 0.4.5 -- VULNERABLE (< 0.4.8)
  2.2.x stream: h2 >= 0.4.8 -- FIXED

Remediation: bump h2 to >= 0.4.8 on the release/0.3.z upstream branch
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix Available? | Notes |
|--------|-----------|-----------------|----------------|-------|
| 2.1.x | Cargo | release/0.3.z | YES | h2 0.4.8 is a released crate; `cargo update -p h2` will pull it in |
| 2.2.x | Cargo | release/0.4.z | N/A | Stream already ships fixed version |

Since the fix is already available upstream (h2 0.4.8 is a published crate), the remediation for the 2.1.x stream uses the **dependency bump** variant: `cargo update -p h2` to pull in >= 0.4.8, followed by downstream propagation to the Konflux release repo.
