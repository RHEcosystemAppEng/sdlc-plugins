# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix (aggregated from all streams)

### Stream 1: 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |

### Stream 2: 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.3 -- Dependency Version Extraction

Lock file inspection results (`git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`):

| Tag | h2 version | Affected? (< 0.4.8) |
|-----|------------|----------------------|
| `v0.3.8` | 0.4.5 | YES |
| `v0.3.12` | 0.4.5 | YES |
| `v0.4.5` | 0.4.8 | NO (>= 0.4.8) |
| `v0.4.8` | 0.4.8 | NO |
| `v0.4.9` | _(retag of v0.4.8)_ | NO (same as v0.4.8) |
| `v0.4.11` | 0.4.9 | NO |
| `v0.4.12` | 0.4.9 | NO |

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-33501 (h2 < 0.4.8):

| Version | Stream | h2 | Affected? | Notes |
|---------|--------|----|-----------|-------|
| 2.1.0 | 2.1.x | 0.4.5 | **YES** | |
| 2.1.1 | 2.1.x | 0.4.5 | **YES** | |
| 2.2.0 | 2.2.x | 0.4.8 | NO | ships fixed version |
| 2.2.1 | 2.2.x | 0.4.8 | NO | ships fixed version |
| 2.2.2 | 2.2.x | -- | NO | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.4.9 | NO | |
| 2.2.4 | 2.2.x | 0.4.9 | NO | |

**Summary**: Mixed impact across streams. The 2.1.x stream ships h2 0.4.5 (vulnerable). The 2.2.x stream ships h2 >= 0.4.8 (fixed) in all versions.

### Dependency Chain Context (Step 2.3.5)

For affected versions (2.1.0, 2.1.1):

```
Dependency chain for h2:
  backend (workspace) -> hyper -> h2
  Profile: production (hyper is a runtime dependency)
  h2 version: 0.4.5 (vulnerable, < 0.4.8)
```

The h2 crate is a transitive dependency pulled in through hyper, the HTTP library used by the backend service. It is a production dependency (not dev-only).

## 2.5 -- Upstream Fix Check

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| 2.1.x | Cargo | `release/0.3.z` | Needs investigation -- h2 0.4.5 was last shipped; upstream branch must be checked for fix |
| 2.2.x | Cargo | `release/0.4.z` | Already ships h2 >= 0.4.8 -- NOT affected |

The upstream fix PR is [hyperium/h2#812](https://github.com/hyperium/h2/pull/812). The fix was released in h2 0.4.8. The 2.1.x stream's upstream branch (`release/0.3.z`) needs to bump h2 to >= 0.4.8 to remediate.
