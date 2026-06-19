# Step 2 -- Version Impact Analysis: CVE-2026-28940

## Version Impact Table

CVE-2026-28940 affects serde_json versions **before 1.0.135**. The fixed version is **1.0.135**.

### Stream 1: 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | serde_json version | Affected? | Notes |
|---------|-----------|-------------------|-----------|-------|
| 2.1.0 | `v0.3.8` | 1.0.137 | NO | Ships fixed version (>= 1.0.135) |
| 2.1.1 | `v0.3.12` | 1.0.137 | NO | Ships fixed version (>= 1.0.135) |

### Stream 2: 2.2.x (rhtpa-release.0.4.z) -- Issue-scoped stream

| Version | Build Tag | serde_json version | Affected? | Notes |
|---------|-----------|-------------------|-----------|-------|
| 2.2.0 | `v0.4.5` | 1.0.138 | NO | Ships fixed version (>= 1.0.135) |
| 2.2.1 | `v0.4.8` | 1.0.138 | NO | Ships fixed version (>= 1.0.135) |
| 2.2.2 | `v0.4.9` | -- | NO | Retag of 2.2.1 (same as 2.2.1: 1.0.138) |
| 2.2.3 | `v0.4.11` | 1.0.139 | NO | Ships fixed version (>= 1.0.135) |
| 2.2.4 | `v0.4.12` | 1.0.139 | NO | Ships fixed version (>= 1.0.135) |

### Combined Summary

| Version | Stream | serde_json | Affected? | Notes |
|---------|--------|-----------|-----------|-------|
| 2.1.0 | 2.1.x | 1.0.137 | NO | |
| 2.1.1 | 2.1.x | 1.0.137 | NO | |
| 2.2.0 | 2.2.x | 1.0.138 | NO | |
| 2.2.1 | 2.2.x | 1.0.138 | NO | |
| 2.2.2 | 2.2.x | -- | NO | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 1.0.139 | NO | |
| 2.2.4 | 2.2.x | 1.0.139 | NO | |

**Result: NO supported versions are affected.** Every shipped version includes serde_json >= 1.0.137, which is above the fixed version threshold of 1.0.135.

## Dependency Chain Context

Not applicable -- no versions are affected, so dependency chain tracing for remediation context is not needed.

## Upstream Fix Status

Not applicable -- the vulnerability is already resolved in all shipped versions. The earliest shipped serde_json version (1.0.137 in the 2.1.x stream) already includes the fix (>= 1.0.135). No upstream backport is needed.
