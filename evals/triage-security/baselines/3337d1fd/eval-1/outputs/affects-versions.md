# Step 3 -- Affects Versions Correction

## Scope

This issue has stream suffix `[rhtpa-2.2]` and is scoped to the **2.2.x** stream.
Only versions belonging to the 2.2.x stream are included in the Affects Versions
correction. Versions from the 2.1.x stream belong to a sibling/companion issue
(see Step 4 cross-stream coordination).

## Current vs Proposed

```
Current Affects Versions:  [RHTPA 2.0.0]
Proposed Affects Versions: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

## Rationale

The PSIRT-assigned Affects Version `RHTPA 2.0.0` is incorrect -- there is no
product version 2.0.0 in the supportability matrix or the Jira version registry
matching the RHTPA prefix. Based on lock file analysis at pinned commits from
the security matrix:

| Version | Build Tag | quinn-proto | Affected? | Include in Affects Versions? |
|---------|-----------|-------------|-----------|------------------------------|
| 2.2.0 | `v0.4.5` | 0.11.9 | YES | YES |
| 2.2.1 | `v0.4.8` | 0.11.12 | YES | YES |
| 2.2.2 | `v0.4.9` | 0.11.12 | YES (retag of 2.2.1) | YES |
| 2.2.3 | `v0.4.11` | 0.11.14 | NO | NO |
| 2.2.4 | `v0.4.12` | 0.11.14 | NO | NO |

Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14, which is at or above the
fix threshold. They are NOT affected and are excluded from Affects Versions.

## Jira Mutation (pending engineer confirmation)

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<jira-id-for-RHTPA-2.2.0>"},
    {"id": "<jira-id-for-RHTPA-2.2.1>"},
    {"id": "<jira-id-for-RHTPA-2.2.2>"}
  ]
})
```

Jira version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields`
(Step 3.1) -- not hardcoded.

## Comment (pending engineer confirmation)

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

RHTPA 2.0.0 does not exist in the supportability matrix. Affected versions
within the 2.2.x stream are 2.2.0, 2.2.1, and 2.2.2 (all ship quinn-proto
< 0.11.14). Versions 2.2.3+ already ship the fixed version (0.11.14).
```

## Cross-Stream Note

The 2.1.x stream (versions 2.1.0, 2.1.1) is also affected (quinn-proto 0.11.9),
but those versions are outside this issue's scope. They would be tracked by a
companion CVE Jira for stream 2.1.x, or addressed via preemptive remediation
tasks (see Step 8, Case B).
