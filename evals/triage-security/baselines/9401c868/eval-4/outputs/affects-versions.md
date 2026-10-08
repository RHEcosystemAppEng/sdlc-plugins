# Step 3 -- Affects Versions Correction: TC-8004

## Current vs Proposed Affects Versions

| | Versions |
|---|---|
| Current (PSIRT-assigned) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Proposed (lock file evidence) | RHTPA 2.1.0, RHTPA 2.1.1 |

## Changes

- **Remove**: RHTPA 2.2.0 -- not affected. Lock file analysis at pinned commit v0.4.5 shows h2 version 0.4.8, which is the fixed version and outside the affected range (< 0.4.8).
- **Add**: RHTPA 2.1.1 -- affected. Lock file analysis at pinned commit v0.3.12 shows h2 version 0.4.5, which is within the affected range (< 0.4.8).

## Rationale

The issue is **unscoped** (no stream suffix), so Affects Versions are corrected across all streams based on lock file evidence:

- **2.1.x stream**: Both versions (2.1.0 and 2.1.1) ship h2 0.4.5, which is vulnerable. Both should be in Affects Versions.
- **2.2.x stream**: All versions (2.2.0 through 2.2.4) ship h2 >= 0.4.8, which is the fixed version. None should be in Affects Versions.

PSIRT originally included RHTPA 2.2.0 because the scan detected h2 as a dependency, but did not verify the shipped version was already at the fix threshold. PSIRT also omitted RHTPA 2.1.1 -- it should be included since it ships the same vulnerable h2 0.4.5 as 2.1.0.

## Proposed Jira Mutation

```
jira.edit_issue("TC-8004", fields={
  "versions": [
    {"name": "RHTPA 2.1.0"},
    {"name": "RHTPA 2.1.1"}
  ]
})
```

Correction comment:
```
Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].
Based on lock file analysis at pinned commits from security-matrix.md.

- Removed RHTPA 2.2.0: ships h2 0.4.8 (fixed version, not affected)
- Added RHTPA 2.1.1: ships h2 0.4.5 (within affected range < 0.4.8)

Issue is unscoped -- correction applies across all streams.
```
