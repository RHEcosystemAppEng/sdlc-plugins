# Step 3 -- Affects Versions Correction: TC-8004

## Current vs Proposed Affects Versions

Since TC-8004 is an **unscoped** issue (no stream suffix), the Affects Versions field should include all affected versions across all streams. Based on the version impact analysis, only the 2.1.x stream versions are affected.

| | Versions |
|---|---|
| Current (PSIRT-assigned) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Proposed (lock file evidence) | RHTPA 2.1.0, RHTPA 2.1.1 |

## Changes

- **Remove**: RHTPA 2.2.0 -- not affected; ships h2 0.4.8 which is at the fix threshold
- **Add**: RHTPA 2.1.1 -- affected; ships h2 0.4.5 which is below the fix threshold of 0.4.8

## Rationale

PSIRT assigned RHTPA 2.1.0 and RHTPA 2.2.0 based on scan-time heuristics. Lock file analysis at the pinned source commits from the supportability matrix shows:

- RHTPA 2.1.0 (build v0.3.8): h2 0.4.5 -- AFFECTED (below 0.4.8 fix threshold)
- RHTPA 2.1.1 (build v0.3.12): h2 0.4.5 -- AFFECTED (below 0.4.8 fix threshold, but was missing from PSIRT assignment)
- RHTPA 2.2.0 (build v0.4.5): h2 0.4.8 -- NOT AFFECTED (at fix threshold)

The correction scopes Affects Versions to only those versions that actually ship the vulnerable dependency, and adds RHTPA 2.1.1 which was missing from the original PSIRT assignment.

## Jira Mutation (proposed)

```
jira.edit_issue("TC-8004", fields={
  "versions": [
    {"name": "RHTPA 2.1.0"},
    {"name": "RHTPA 2.1.1"}
  ]
})

jira.add_comment("TC-8004", "Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].
Based on lock file analysis at pinned commits from security-matrix.md.
RHTPA 2.2.0 removed (ships h2 0.4.8, at fix threshold). RHTPA 2.1.1 added (ships h2 0.4.5, below fix threshold).
Issue is unscoped -- correction includes all affected versions across all streams.")
```
