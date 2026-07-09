# Step 2 -- Version Impact Analysis for CVE-2026-31812

## Version Impact Table

CVE-2026-31812 (quinn-proto < 0.11.14), scoped to 2.2.x stream:

| Version | Stream | Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | 0.11.12 | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | |

All versions from both streams in the supportability matrix are included. Version impact uses pinned commit tags from the supportability matrix for each version.

### Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency
  Profile: production (quinn-proto is a runtime dependency for QUIC transport)

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml
```
