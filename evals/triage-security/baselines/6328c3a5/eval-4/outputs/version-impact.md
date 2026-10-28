# Version Impact Analysis — TC-8004

## CVE-2026-33501 (h2 < 0.4.8)

### Version Impact Table

| Version | Stream | Build Tag | h2 version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.4.5 | **YES** | < 0.4.8 |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.4.5 | **YES** | < 0.4.8 |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.4.8 | NO | >= 0.4.8 (fixed) |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.4.8 | NO | >= 0.4.8 (fixed) |
| 2.2.2 | 2.2.x | `v0.4.9` | _(retag)_ | NO | same as 2.2.1 |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.4.9 | NO | >= 0.4.8 (fixed) |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.4.9 | NO | >= 0.4.8 (fixed) |

### Stream Impact Summary

| Stream | Affected Versions | Unaffected Versions | Overall Impact |
|--------|-------------------|---------------------|----------------|
| 2.1.x | 2.1.0, 2.1.1 | _(none)_ | **AFFECTED** — all versions ship h2 0.4.5 (vulnerable) |
| 2.2.x | _(none)_ | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 | **NOT AFFECTED** — all versions ship h2 >= 0.4.8 (fixed) |

### Mixed Impact Across Streams

This vulnerability has **mixed impact** across the two version streams:

- **2.1.x stream**: All released versions (2.1.0 and 2.1.1) ship h2 0.4.5, which is within the affected range (< 0.4.8). Remediation is required.
- **2.2.x stream**: All released versions ship h2 >= 0.4.8 (the fixed version). The earliest 2.2.x version (2.2.0, build v0.4.5) already ships h2 0.4.8. No remediation is needed.

### Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> h2
  Type: assumed direct dependency (based on Cargo ecosystem mapping)
  Profile: production (h2 is a runtime HTTP/2 library)

  Present in: 2.1.x (h2 0.4.5), 2.2.x (h2 >= 0.4.8)
  Vulnerable in: 2.1.x only
```

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Latest Released h2 | Fix Available? | Notes |
|--------|-----------|-----------------|---------------------|----------------|-------|
| 2.1.x | Cargo | `release/0.3.z` | 0.4.5 (at v0.3.12) | Unknown | Latest released build ships vulnerable version; upstream branch HEAD not checked in this eval |
| 2.2.x | Cargo | `release/0.4.z` | 0.4.8+ (at all tags) | YES | All released versions already ship the fix |
