# Step 3 - Affects Versions Correction: TC-8001

## Stream Scope

This issue is scoped to stream **2.2.x** (from summary suffix `[rhtpa-2.2]`).
Only 2.2.x versions are included in the Affects Versions correction.
The 2.1.x stream impact is handled separately via cross-stream coordination (Step 4.2 / Step 7 Case B).

## Current vs Proposed Affects Versions

| | Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.0.0 |
| **Proposed (lock file evidence)** | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

## Correction Rationale

The PSIRT-assigned Affects Version `RHTPA 2.0.0` is **incorrect**:
- There is no `2.0.x` version stream in the Version Streams configuration
- Lock file analysis at pinned commits from security-matrix.md shows:
  - **RHTPA 2.2.0** (tag `v0.4.5`): quinn-proto 0.11.9 - AFFECTED (< 0.11.14)
  - **RHTPA 2.2.1** (tag `v0.4.8`): quinn-proto 0.11.12 - AFFECTED (< 0.11.14)
  - **RHTPA 2.2.2** (tag `v0.4.9`): retag of 2.2.1 - AFFECTED (same as 2.2.1)
  - **RHTPA 2.2.3** (tag `v0.4.11`): quinn-proto 0.11.14 - NOT affected (>= fix)
  - **RHTPA 2.2.4** (tag `v0.4.12`): quinn-proto 0.11.14 - NOT affected (>= fix)

## Proposed Jira Mutation

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"name": "RHTPA 2.2.0"},
    {"name": "RHTPA 2.2.1"},
    {"name": "RHTPA 2.2.2"}
  ]
})
```

Note: Version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` at runtime. Version names from the supportability matrix are used here; actual Jira version IDs are resolved at execution time.

## Proposed Comment

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

Evidence:
- RHTPA 2.2.0 (v0.4.5): quinn-proto 0.11.9 (affected, < 0.11.14)
- RHTPA 2.2.1 (v0.4.8): quinn-proto 0.11.12 (affected, < 0.11.14)
- RHTPA 2.2.2 (v0.4.9): retag of 2.2.1 (affected, same as 2.2.1)
- RHTPA 2.2.3 (v0.4.11): quinn-proto 0.11.14 (not affected, ships fix)
- RHTPA 2.2.4 (v0.4.12): quinn-proto 0.11.14 (not affected, ships fix)
```

## Cross-Stream Impact Note

Versions in the **2.1.x stream** are also affected but are outside this issue's scope:
- RHTPA 2.1.0 (tag `v0.3.8`): quinn-proto 0.11.9 - AFFECTED
- RHTPA 2.1.1 (tag `v0.3.12`): quinn-proto 0.11.9 - AFFECTED

These are handled via Step 7 Case B (cross-stream impact / preemptive remediation).
