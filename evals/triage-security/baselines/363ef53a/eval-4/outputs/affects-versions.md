# Affects Versions Correction — TC-8004

## Current vs. Proposed Affects Versions

Since TC-8004 is **unscoped** (no stream suffix), the Affects Versions correction includes all affected versions across all streams.

| | Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.1.0, RHTPA 2.2.0 |
| **Proposed (lock file evidence)** | RHTPA 2.1.0, RHTPA 2.1.1 |

## Correction Details

- **RHTPA 2.1.0**: KEEP — h2 0.4.5 is within the affected range (< 0.4.8). Confirmed via `git show v0.3.8:Cargo.lock`.
- **RHTPA 2.1.1**: ADD — h2 0.4.5 is within the affected range (< 0.4.8). Confirmed via `git show v0.3.12:Cargo.lock`. PSIRT did not include this version.
- **RHTPA 2.2.0**: REMOVE — h2 0.4.8 is at the fix threshold (>= 0.4.8, NOT affected). Confirmed via `git show v0.4.5:Cargo.lock`. PSIRT incorrectly included this version.

## Rationale

PSIRT assigned Affects Versions based on scan time, not actual dependency analysis. Lock file inspection at pinned source commits shows:

- The 2.1.x stream (versions 2.1.0 and 2.1.1) ships h2 0.4.5, which is below the fix threshold of 0.4.8. Both versions are affected.
- The 2.2.x stream (versions 2.2.0 through 2.2.4) ships h2 0.4.8 or later, which is at or above the fix threshold. No 2.2.x versions are affected.

The correction removes RHTPA 2.2.0 (not affected) and adds RHTPA 2.1.1 (affected but missing from PSIRT's assignment).

## Jira Mutation (proposed)

```
jira.edit_issue("TC-8004", fields={
  "versions": [
    {"id": "<RHTPA-2.1.0-jira-id>"},
    {"id": "<RHTPA-2.1.1-jira-id>"}
  ]
})
```

Version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (not hardcoded).

## Comment (proposed)

```
Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].
Based on lock file analysis at pinned commits from security-matrix.md.

- RHTPA 2.1.0: h2 0.4.5 (affected, < 0.4.8)
- RHTPA 2.1.1: h2 0.4.5 (affected, < 0.4.8) — added
- RHTPA 2.2.0: h2 0.4.8 (NOT affected, >= 0.4.8) — removed

This issue is unscoped (no stream suffix); correction covers all streams.
```
