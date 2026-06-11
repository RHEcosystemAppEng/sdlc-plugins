# Step 3 -- Affects Versions Correction

## Current vs Proposed

- **Current Affects Versions (PSIRT-assigned):** RHTPA 2.0.0
- **Proposed Affects Versions (lock-file-verified):** RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

## Rationale

The PSIRT-assigned value `RHTPA 2.0.0` is incorrect. There is no 2.0.x version in the supportability matrix, and the issue is scoped to the 2.2.x stream per the summary suffix `[rhtpa-2.2]`.

Lock file analysis at pinned commits from the supportability matrix shows:

| Version | Tag | quinn-proto | Affected? |
|---------|-----|-------------|-----------|
| 2.2.0 | `v0.4.5` | 0.11.9 | YES -- 0.11.9 < 0.11.14 |
| 2.2.1 | `v0.4.8` | 0.11.12 | YES -- 0.11.12 < 0.11.14 |
| 2.2.2 | `v0.4.9` | (0.11.12) | YES -- retag of 2.2.1, same as 2.2.1 |
| 2.2.3 | `v0.4.11` | 0.11.14 | NO -- ships fixed version |
| 2.2.4 | `v0.4.12` | 0.11.14 | NO -- ships fixed version |

Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (the fixed version) and are NOT affected.

## PROPOSAL: Jira Mutation (not executed)

Replace the Affects Versions field on TC-8001:

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

The Jira version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (version names referenced here, not hardcoded IDs). The API call would be:

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"name": "RHTPA 2.2.0"},
    {"name": "RHTPA 2.2.1"},
    {"name": "RHTPA 2.2.2"}
  ]
})
```

Note: In a live triage, the `name` values above would be resolved to Jira version `id` values discovered at runtime from the `allowedValues` of the `versions` field. No hardcoded IDs are used.

## PROPOSAL: Jira Comment (not executed)

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

Evidence:
- 2.2.0 (v0.4.5): quinn-proto 0.11.9 -- affected (< 0.11.14)
- 2.2.1 (v0.4.8): quinn-proto 0.11.12 -- affected (< 0.11.14)
- 2.2.2 (v0.4.9): retag of 2.2.1 -- affected (same as 2.2.1)
- 2.2.3 (v0.4.11): quinn-proto 0.11.14 -- NOT affected (fixed version)
- 2.2.4 (v0.4.12): quinn-proto 0.11.14 -- NOT affected (fixed version)
```
