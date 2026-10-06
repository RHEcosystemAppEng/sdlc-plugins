# Affects Versions Correction -- TC-8004

## Step 3 -- Affects Versions Correction

### Current vs Proposed

The issue is **unscoped** (no stream suffix), so the Affects Versions correction
includes all affected versions across all streams.

| | Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.1.0, RHTPA 2.2.0 |
| **Proposed (lock file evidence)** | RHTPA 2.1.0, RHTPA 2.1.1 |

### Correction Details

- **RHTPA 2.1.0**: KEEP -- h2 0.4.5 is vulnerable (< 0.4.8). Confirmed via `git show v0.3.8:Cargo.lock`.
- **RHTPA 2.1.1**: ADD -- h2 0.4.5 is vulnerable (< 0.4.8). Confirmed via `git show v0.3.12:Cargo.lock`. This version was missing from the PSIRT-assigned Affects Versions.
- **RHTPA 2.2.0**: REMOVE -- h2 0.4.8 is the fixed version (>= 0.4.8). Confirmed via `git show v0.4.5:Cargo.lock`. PSIRT incorrectly included this version.

### Rationale

PSIRT assigned Affects Versions based on scan time, not actual dependency analysis.
Lock file inspection at each version's pinned source commit shows that:

1. The 2.1.x stream (builds v0.3.8 and v0.3.12) ships h2 0.4.5, which is within the
   vulnerable range (< 0.4.8).
2. The 2.2.x stream ships h2 >= 0.4.8 across all versions, starting from its first
   release (2.2.0). RHTPA 2.2.0 should be removed from Affects Versions.
3. RHTPA 2.1.1 was missing from the original Affects Versions despite being affected.

### Jira Mutation (proposed)

```
jira.edit_issue("TC-8004", fields={
  "versions": [
    {"id": "<RHTPA-2.1.0-jira-id>"},
    {"id": "<RHTPA-2.1.1-jira-id>"}
  ]
})
```

Version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` in
a live triage (Step 3.1). Only versions matching the Jira version prefix "RHTPA" and
confirmed affected by lock file analysis are included.

### Comment (proposed)

```
Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].
Based on lock file analysis at pinned commits from security-matrix.md.

Changes:
- Removed RHTPA 2.2.0: ships h2 0.4.8 (fixed version, not affected)
- Added RHTPA 2.1.1: ships h2 0.4.5 (vulnerable, was missing)

This issue is unscoped (no stream suffix) -- correction covers all streams.
```
