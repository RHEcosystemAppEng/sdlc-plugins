# Step 3 -- Affects Versions Correction

## Current vs Proposed Affects Versions

The issue is **unscoped** (no stream suffix), so Affects Versions should include all affected versions across all streams.

**Current (PSIRT-assigned)**: RHTPA 2.1.0, RHTPA 2.2.0
**Proposed (based on lock file analysis)**: RHTPA 2.1.0, RHTPA 2.1.1

## Correction Details

| Version | Currently Listed? | Actually Affected? | Action |
|---------|-------------------|--------------------|--------|
| RHTPA 2.1.0 | Yes | YES (h2 0.4.5 < 0.4.8) | Keep |
| RHTPA 2.1.1 | No | YES (h2 0.4.5 < 0.4.8) | Add |
| RHTPA 2.2.0 | Yes | NO (h2 0.4.8 >= 0.4.8) | Remove |

## Rationale

- **RHTPA 2.1.0**: Correctly included by PSIRT. Lock file at tag v0.3.8 shows h2 0.4.5, which is within the affected range (< 0.4.8).
- **RHTPA 2.1.1**: Missing from PSIRT assignment. Lock file at tag v0.3.12 shows h2 0.4.5, which is within the affected range (< 0.4.8). Must be added.
- **RHTPA 2.2.0**: Incorrectly included by PSIRT. Lock file at tag v0.4.5 shows h2 0.4.8, which is at the fix threshold (>= 0.4.8). Must be removed.
- **RHTPA 2.2.1 through 2.2.4**: Not listed by PSIRT, correctly excluded. All ship h2 >= 0.4.8.

## Proposed Jira Update

```
jira.edit_issue("TC-8004", fields={
  "versions": [
    {"name": "RHTPA 2.1.0"},
    {"name": "RHTPA 2.1.1"}
  ]
})
```

## Comment

Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].
Based on lock file analysis at pinned commits from security-matrix.md.
- Removed RHTPA 2.2.0: h2 0.4.8 at tag v0.4.5 is at or above fix threshold (0.4.8).
- Added RHTPA 2.1.1: h2 0.4.5 at tag v0.3.12 is below fix threshold (0.4.8).
Issue is unscoped -- Affects Versions include all affected versions across all streams.
