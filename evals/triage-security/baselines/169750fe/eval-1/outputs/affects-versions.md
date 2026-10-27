# Step 3 -- Affects Versions Correction

## Current State

- **Issue**: TC-8001
- **Issue stream scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **Current Affects Versions**: RHTPA 2.0.0
- **PSIRT-assigned version**: RHTPA 2.0.0

## Version Impact (scoped to 2.2.x stream)

From the version impact analysis, the following 2.2.x versions are affected:

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.2.0 | 0.11.9 | YES |
| 2.2.1 | 0.11.12 | YES |
| 2.2.2 | -- (retag of 2.2.1) | YES |
| 2.2.3 | 0.11.14 | NO |
| 2.2.4 | 0.11.14 | NO |

Note: 2.1.x versions (2.1.0, 2.1.1) are also affected but are excluded from
this correction because the issue is scoped to the 2.2.x stream. The 2.1.x
versions belong to a sibling issue (if one exists) or will be addressed via
Case A cross-stream impact handling.

## Proposed Correction

**PSIRT version is wrong**: RHTPA 2.0.0 does not correspond to any configured
version stream (no 2.0.x stream exists in the Version Streams table).

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

### Rationale

- **RHTPA 2.0.0** is removed because there is no 2.0.x version stream
  configured in Security Configuration. This version does not exist in the
  supportability matrix.
- **RHTPA 2.2.0** is added because it ships quinn-proto 0.11.9, which is
  within the affected range (< 0.11.14).
- **RHTPA 2.2.1** is added because it ships quinn-proto 0.11.12, which is
  within the affected range (< 0.11.14).
- **RHTPA 2.2.2** is added because it is a retag of 2.2.1 and ships the same
  quinn-proto 0.11.12 (within the affected range).
- **RHTPA 2.2.3** and **RHTPA 2.2.4** are excluded because they ship
  quinn-proto 0.11.14, which is the fixed version (>= 0.11.14, not affected).

## Proposed Jira Operation (not executed)

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<jira-version-id-for-RHTPA-2.2.0>"},
    {"id": "<jira-version-id-for-RHTPA-2.2.1>"},
    {"id": "<jira-version-id-for-RHTPA-2.2.2>"}
  ]
})
```

Version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields`
(Step 3.1). No hardcoded IDs are used.

## Proposed Comment (not executed)

A comment would be posted to TC-8001 documenting the correction:

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

RHTPA 2.0.0 removed: no 2.0.x version stream exists.
RHTPA 2.2.0 added: ships quinn-proto 0.11.9 (affected).
RHTPA 2.2.1 added: ships quinn-proto 0.11.12 (affected).
RHTPA 2.2.2 added: retag of 2.2.1 (same quinn-proto 0.11.12, affected).
RHTPA 2.2.3 and 2.2.4 excluded: ship quinn-proto 0.11.14 (fixed).
```

Note: No ProdSec Jira account ID is configured, so no @mention is included.
