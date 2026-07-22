# Affects Versions Correction -- TC-8004

## Current vs Proposed

Since TC-8004 is **unscoped** (no stream suffix), the Affects Versions field should include all affected versions across all streams, not just one per stream.

| | Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.1.0, RHTPA 2.2.0 |
| **Proposed (lock file evidence)** | RHTPA 2.1.0, RHTPA 2.1.1 |

### Changes Required

| Action | Version | Reason |
|--------|---------|--------|
| **Keep** | RHTPA 2.1.0 | Affected -- ships h2 0.4.5 (< 0.4.8) |
| **Add** | RHTPA 2.1.1 | Affected -- ships h2 0.4.5 (< 0.4.8), missing from PSIRT assignment |
| **Remove** | RHTPA 2.2.0 | Not affected -- ships h2 0.4.8 (>= 0.4.8, the fix version) |

### Rationale

PSIRT assigned Affects Versions based on scan time, not actual dependency analysis. Lock file inspection at pinned source commits from `security-matrix.md` shows:

- **RHTPA 2.1.0** (tag `v0.3.8`): h2 = 0.4.5 -- VULNERABLE (below fix threshold 0.4.8)
- **RHTPA 2.1.1** (tag `v0.3.12`): h2 = 0.4.5 -- VULNERABLE (below fix threshold 0.4.8) -- **was missing from PSIRT assignment**
- **RHTPA 2.2.0** (tag `v0.4.5`): h2 = 0.4.8 -- NOT VULNERABLE (at or above fix threshold 0.4.8) -- **incorrectly included by PSIRT**

All other 2.2.x versions (2.2.1 through 2.2.4) ship h2 0.4.8 or 0.4.9 and are also not affected.

### Proposed Jira Update

```
jira.edit_issue("TC-8004", fields={
  "versions": [
    {"name": "RHTPA 2.1.0"},
    {"name": "RHTPA 2.1.1"}
  ]
})
```

### Proposed Jira Comment

```
Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].

Changes:
- Added RHTPA 2.1.1: ships h2 0.4.5, below fix threshold 0.4.8
- Removed RHTPA 2.2.0: ships h2 0.4.8, at or above fix threshold 0.4.8

Based on lock file analysis at pinned commits from security-matrix.md.
This issue is unscoped (no stream suffix) -- correction includes all affected versions across all streams.
Only the 2.1.x stream is affected; the 2.2.x stream ships the patched version.
```
