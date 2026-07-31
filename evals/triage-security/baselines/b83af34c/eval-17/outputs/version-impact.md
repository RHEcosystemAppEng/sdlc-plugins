# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

### Issue Stream Scope: 2.2.x (from summary suffix `[rhtpa-2.2]`)

Note: The issue is scoped to stream 2.2.x, but version impact is analyzed across all configured streams for cross-stream awareness (Case A evaluation).

### Version Impact Table

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | 2.1.x | 0.11.9 | YES | < 0.11.14 |
| 2.2.0 | 2.2.x | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 2.2.x | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | 2.2.x | 0.11.14 | NO | >= 0.11.14 (fixed) |

### Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (Cargo)
  Profile: production (quinn-proto is a runtime dependency)

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml/Cargo.lock
```

### Cross-Stream Impact Summary

- **2.1.x stream**: versions 2.1.0, 2.1.1 are affected (quinn-proto 0.11.9 < 0.11.14)
- **2.2.x stream** (this issue's scope): versions 2.2.0, 2.2.1, 2.2.2 are affected; versions 2.2.3, 2.2.4 are NOT affected

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | Needs verification |
| 2.2.x | Cargo | release/0.4.z | Needs verification |

### Affects Versions Correction (Step 3)

- Current (PSIRT-assigned): `[RHTPA 2.0.0]`
- RHTPA 2.0.0 does not exist in the configured version streams -- PSIRT version is wrong
- Proposed (scoped to 2.2.x stream): `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
- Versions 2.2.3 and 2.2.4 are NOT affected (ship quinn-proto 0.11.14, which is the fix version)
