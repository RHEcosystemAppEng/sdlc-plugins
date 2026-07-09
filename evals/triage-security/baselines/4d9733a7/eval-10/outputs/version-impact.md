# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-55123 (tokio < 1.42.0)

### Current stream (rhtpa-2.2, scoped)

| Version | tokio version | Affected? | Notes |
|---------|---------------|-----------|-------|
| 2.2.0 | 1.41.1 | YES | |
| 2.2.1 | 1.41.1 | YES | |

### Cross-stream analysis (rhtpa-2.1)

| Version | tokio version | Affected? | Notes |
|---------|---------------|-----------|-------|
| 2.1.0 | 1.40.0 | YES | |
| 2.1.1 | 1.40.0 | YES | |

## Cross-Stream Impact Summary

Both streams (rhtpa-2.1 and rhtpa-2.2) ship tokio versions below the fix threshold of 1.42.0.

- **rhtpa-2.2** (current stream): 2.2.0 and 2.2.1 ship tokio 1.41.1 -- AFFECTED
- **rhtpa-2.1** (other stream): 2.1.0 and 2.1.1 ship tokio 1.40.0 -- AFFECTED

Since this issue is scoped to rhtpa-2.2, the cross-stream impact on rhtpa-2.1 will be handled via Step 8 Case B (proactive preemptive remediation).

## Dependency Chain Context

```
Dependency chain for tokio:
  backend (workspace) -> tokio
  Type: direct dependency
  Profile: production (tokio is a runtime dependency)

Remediation: bump tokio to >= 1.42.0 in Cargo.toml
```
