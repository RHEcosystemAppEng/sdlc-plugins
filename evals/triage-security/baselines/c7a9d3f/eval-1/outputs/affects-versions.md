# Step 3 -- Affects Versions Correction: TC-8001

## Current Affects Versions (PSIRT-assigned)

- RHTPA 2.0.0

## Issue Stream Scope

This issue is scoped to stream **2.2.x** (per summary suffix `[rhtpa-2.2]`). Only versions belonging to the 2.2.x stream should be included in the Affects Versions for this issue.

## Version Impact (scoped to 2.2.x stream)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| RHTPA 2.2.0 | 0.11.9 | YES |
| RHTPA 2.2.1 | 0.11.12 | YES |
| RHTPA 2.2.2 | -- | YES (retag of 2.2.1) |
| RHTPA 2.2.3 | 0.11.14 | NO (fixed) |
| RHTPA 2.2.4 | 0.11.14 | NO (fixed) |

## Proposed Correction

The PSIRT-assigned Affects Version "RHTPA 2.0.0" is incorrect -- there is no 2.0.x stream in the Version Streams configuration. The correct Affects Versions, based on lock file analysis at pinned commits from the security matrix, are the 2.2.x versions that ship a vulnerable quinn-proto (< 0.11.14).

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

### Rationale

- **RHTPA 2.0.0**: REMOVED -- no 2.0.x version stream exists; this was a PSIRT assignment error
- **RHTPA 2.2.0**: ADDED -- ships quinn-proto 0.11.9 (vulnerable, < 0.11.14)
- **RHTPA 2.2.1**: ADDED -- ships quinn-proto 0.11.12 (vulnerable, < 0.11.14)
- **RHTPA 2.2.2**: ADDED -- retag of 2.2.1, same source as 2.2.1 (vulnerable)
- **RHTPA 2.2.3**: NOT included -- ships quinn-proto 0.11.14 (fixed version)
- **RHTPA 2.2.4**: NOT included -- ships quinn-proto 0.11.14 (fixed version)

### Versions NOT included (outside stream scope)

The following versions from the 2.1.x stream are also affected but belong to a different stream scope. They would be tracked by a separate sibling Vulnerability issue for stream 2.1.x:

- RHTPA 2.1.0: ships quinn-proto 0.11.9 (vulnerable)
- RHTPA 2.1.1: ships quinn-proto 0.11.9 (vulnerable)

## Proposed Jira Mutation

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<jira-id-for-RHTPA-2.2.0>"},
    {"id": "<jira-id-for-RHTPA-2.2.1>"},
    {"id": "<jira-id-for-RHTPA-2.2.2>"}
  ]
})
```

Note: Jira version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` in a live triage. The IDs shown above are placeholders.

## Proposed Comment

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

Evidence:
- RHTPA 2.2.0 (tag v0.4.5): quinn-proto 0.11.9 (vulnerable)
- RHTPA 2.2.1 (tag v0.4.8): quinn-proto 0.11.12 (vulnerable)
- RHTPA 2.2.2 (tag v0.4.9): retag of 2.2.1 (vulnerable)
- RHTPA 2.2.3 (tag v0.4.11): quinn-proto 0.11.14 (fixed -- not affected)
- RHTPA 2.2.4 (tag v0.4.12): quinn-proto 0.11.14 (fixed -- not affected)

RHTPA 2.0.0 removed: no 2.0.x version stream exists in the product configuration.
```
