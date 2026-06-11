# Step 3 -- Affects Versions Correction

## Current State

- **Current Affects Versions (PSIRT-assigned)**: RHTPA 2.0.0
- **Issue stream scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)

## Stream-Scoped Version Impact

Since this issue is scoped to the 2.2.x stream, only versions from that stream are included in the Affects Versions correction. The 2.1.x stream versions (2.1.0, 2.1.1) are out of scope for this issue -- they would be tracked by a separate companion Vulnerability issue for stream 2.1.x.

Affected versions within the 2.2.x stream (from the version impact table):

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.2.0 | 0.11.9 | YES |
| 2.2.1 | 0.11.12 | YES |
| 2.2.2 | -- (retag of 2.2.1) | YES |
| 2.2.3 | 0.11.14 | NO |
| 2.2.4 | 0.11.14 | NO |

## Proposed Correction

```
Current: [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

**Rationale**: The PSIRT-assigned Affects Version "RHTPA 2.0.0" is incorrect -- there is no 2.0.x version stream configured, and this version does not appear in any supportability matrix. Based on lock file analysis at pinned commits from security-matrix.md, the actually affected versions in the 2.2.x stream are RHTPA 2.2.0, RHTPA 2.2.1, and RHTPA 2.2.2. Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (the fixed version) and are NOT affected.

## Proposed Jira Mutation (requires engineer confirmation)

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<RHTPA-2.2.0-jira-id>"},
    {"id": "<RHTPA-2.2.1-jira-id>"},
    {"id": "<RHTPA-2.2.2-jira-id>"}
  ]
})
```

Note: Jira version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` -- not hardcoded. The IDs shown above are placeholders.

## Proposed Comment

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

- RHTPA 2.2.0 (tag v0.4.5): quinn-proto 0.11.9 -- AFFECTED
- RHTPA 2.2.1 (tag v0.4.8): quinn-proto 0.11.12 -- AFFECTED
- RHTPA 2.2.2 (tag v0.4.9): retag of 2.2.1 -- AFFECTED
- RHTPA 2.2.3 (tag v0.4.11): quinn-proto 0.11.14 -- NOT affected (fixed version)
- RHTPA 2.2.4 (tag v0.4.12): quinn-proto 0.11.14 -- NOT affected (fixed version)

RHTPA 2.0.0 was removed: no 2.0.x version stream exists in the supportability matrix.
```

## Cross-Stream Impact Notice

The version impact analysis reveals that the **2.1.x stream** is also affected:
- RHTPA 2.1.0 (tag v0.3.8): quinn-proto 0.11.9 -- AFFECTED
- RHTPA 2.1.1 (tag v0.3.12): quinn-proto 0.11.9 -- AFFECTED

These are outside this issue's scope (scoped to 2.2.x). A cross-stream impact comment would be posted to TC-8001:

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis.
- RHTPA 2.1.0: quinn-proto 0.11.9
- RHTPA 2.1.1: quinn-proto 0.11.9
This stream is tracked by a companion issue (see Related links) or may require separate PSIRT triage.
```
