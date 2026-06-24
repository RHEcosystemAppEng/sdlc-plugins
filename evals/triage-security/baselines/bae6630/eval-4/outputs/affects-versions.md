# Affects Versions Correction -- TC-8004

## Current vs Corrected Affects Versions

| | Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.1.0, RHTPA 2.2.0 |
| **Proposed (lock file evidence)** | RHTPA 2.1.0, RHTPA 2.1.1 |

## Correction Details

The PSIRT-assigned Affects Versions are **incorrect**:

1. **RHTPA 2.2.0 should be REMOVED** -- lock file analysis shows 2.2.0 ships h2 0.4.8, which is at the fix threshold (>= 0.4.8). This version is NOT affected.
2. **RHTPA 2.1.1 should be ADDED** -- lock file analysis shows 2.1.1 ships h2 0.4.5, which is below the fix threshold. This version IS affected but was not included by PSIRT.

### Evidence

| Version | h2 Version (from Cargo.lock) | Fix Threshold | Affected? | In Current AV? | Action |
|---------|------------------------------|---------------|-----------|-----------------|--------|
| RHTPA 2.1.0 | 0.4.5 | 0.4.8 | YES | Yes | Keep |
| RHTPA 2.1.1 | 0.4.5 | 0.4.8 | YES | No | **Add** |
| RHTPA 2.2.0 | 0.4.8 | 0.4.8 | NO | Yes | **Remove** |
| RHTPA 2.2.1 | 0.4.8 | 0.4.8 | NO | No | Correct (not listed) |
| RHTPA 2.2.2 | _(retag of 2.2.1)_ | 0.4.8 | NO | No | Correct (not listed) |
| RHTPA 2.2.3 | 0.4.9 | 0.4.8 | NO | No | Correct (not listed) |
| RHTPA 2.2.4 | 0.4.9 | 0.4.8 | NO | No | Correct (not listed) |

### Scope Note

Since TC-8004 is **unscoped** (no stream suffix), the Affects Versions correction includes all affected versions across all streams. Only versions from the 2.1.x stream are actually affected:

- **2.1.x stream**: RHTPA 2.1.0 and RHTPA 2.1.1 are affected (h2 0.4.5)
- **2.2.x stream**: No versions are affected (all ship h2 >= 0.4.8)

### Proposed Jira Update

```
Current:  [RHTPA 2.1.0, RHTPA 2.2.0]
Proposed: [RHTPA 2.1.0, RHTPA 2.1.1]

Changes:
  - Remove: RHTPA 2.2.0 (not affected -- ships h2 0.4.8)
  - Add:    RHTPA 2.1.1 (affected -- ships h2 0.4.5)
```

### Jira Comment (to be posted after confirmation)

```
Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].
Based on lock file analysis at pinned commits from security-matrix.md.

RHTPA 2.2.0 removed: ships h2 0.4.8 (at fix threshold, not affected).
RHTPA 2.1.1 added: ships h2 0.4.5 (below fix threshold 0.4.8, affected).

This issue is unscoped (no stream suffix) -- Affects Versions include all affected versions across all streams.
```
