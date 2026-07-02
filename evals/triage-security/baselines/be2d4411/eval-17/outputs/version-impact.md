# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Version | Stream | Backend Tag | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Stream Scope Summary

This issue is scoped to stream **2.2.x** (per summary suffix `[rhtpa-2.2]`).

**Within scope (2.2.x):**
- Affected: 2.2.0, 2.2.1, 2.2.2
- Not affected: 2.2.3, 2.2.4

**Outside scope (2.1.x):**
- Affected: 2.1.0, 2.1.1
- These versions are tracked by companion issues or require separate PSIRT triage (Case B cross-stream impact).

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for quinn-proto (Cargo):
  Ecosystem: Cargo (Rust crate)
  Lock file: Cargo.lock
  Check command: git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'

  First affected in 2.2.x: 2.2.0 (tag v0.4.5, quinn-proto 0.11.9)
  Fixed in 2.2.x from: 2.2.3 (tag v0.4.11, quinn-proto 0.11.14)
```

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Backend Tag at Latest | quinn-proto at Latest | Fixed? |
|--------|-----------|-----------------|----------------------|----------------------|--------|
| 2.2.x | Cargo | release/0.4.z | v0.4.12 | 0.11.14 | YES |
| 2.1.x | Cargo | release/0.3.z | v0.3.12 | 0.11.9 | NO |

Stream 2.2.x has the fix at the latest released version (v0.4.12 ships quinn-proto 0.11.14). The upstream branch `release/0.4.z` already contains the fix.

Stream 2.1.x does NOT have the fix -- the latest release (v0.3.12) still ships quinn-proto 0.11.9. Remediation for 2.1.x would require an upstream backport to `release/0.3.z`.

## Affects Versions Correction (Step 3)

PSIRT assigned: `RHTPA 2.0.0`
This is incorrect -- RHTPA 2.0.0 does not exist in any configured Version Stream.

Scoped to stream 2.2.x, the correct Affects Versions based on lock file evidence:
- **Proposed**: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Correction: `Current: [RHTPA 2.0.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Note: Version 2.2.2 is a retag of 2.2.1 (identical backend source at v0.4.8) and ships the same vulnerable quinn-proto 0.11.12. It is included in Affects Versions because it ships vulnerable code.
