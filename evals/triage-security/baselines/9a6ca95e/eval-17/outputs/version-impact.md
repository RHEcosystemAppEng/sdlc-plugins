# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Stream | Version | Build | Backend Tag | quinn-proto | Affected? | Notes |
|--------|---------|-------|-------------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | 0.3.8 | `v0.3.8` | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | 0.3.12 | `v0.3.12` | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | 0.4.5 | `v0.4.5` | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | 0.4.8 | `v0.4.8` | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | 0.4.9 | `v0.4.8` | 0.11.12 | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.x | 2.2.3 | 0.4.11 | `v0.4.11` | 0.11.14 | NO | fixed version shipped |
| 2.2.x | 2.2.4 | 0.4.12 | `v0.4.12` | 0.11.14 | NO | fixed version shipped |

## Dependency Chain Context

```
Dependency chain for quinn-proto (Cargo):
  Ecosystem: Cargo (Rust crate)
  Lock file: Cargo.lock
  Check command: git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'

  Stream 2.1.x: quinn-proto 0.11.9 present in all versions (v0.3.8, v0.3.12)
  Stream 2.2.x: quinn-proto 0.11.9 in 2.2.0, upgraded to 0.11.12 in 2.2.1-2.2.2,
                 then upgraded to 0.11.14 (fixed) in 2.2.3+
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix Threshold | Status |
|--------|-----------|-----------------|---------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.14 | Needs verification (upstream branch HEAD not checked in simulated data) |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | FIXED in stream (2.2.3+ ship 0.11.14) |

## Stream-Scoped Analysis (Issue Scope: 2.2.x)

This issue is scoped to the **2.2.x** stream (from summary suffix `[rhtpa-2.2]`).

**In-scope stream (2.2.x):**
- Versions 2.2.0, 2.2.1, 2.2.2 are affected (ship quinn-proto < 0.11.14)
- Versions 2.2.3, 2.2.4 are NOT affected (ship quinn-proto 0.11.14, the fixed version)
- The fix is already present in the latest releases of this stream
- Affects Versions should be set to: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

**Out-of-scope stream (2.1.x) -- Cross-stream impact:**
- ALL versions (2.1.0, 2.1.1) are affected (ship quinn-proto 0.11.9)
- No version in the 2.1.x stream ships the fix
- This stream requires remediation (Case B: cross-stream proactive)

## Affects Versions Correction Required

Current Jira Affects Versions: **RHTPA 2.0.0** (incorrect -- no 2.0.x stream exists)

Corrected Affects Versions for the 2.2.x scope: **RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2**

The PSIRT-assigned version RHTPA 2.0.0 does not correspond to any configured version stream. The actual affected versions in the 2.2.x stream are 2.2.0 through 2.2.2, based on lock file evidence showing quinn-proto versions below the 0.11.14 fix threshold.
