# Step 3 -- Affects Versions Correction for TC-8005

## Current vs Proposed Affects Versions

The issue is scoped to the **2.2.x** stream per the `[rhtpa-2.2]` suffix. Only versions belonging to the 2.2.x stream are included in the correction. The 2.1.x stream versions (also affected) belong to a sibling issue.

| | Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.0.0 |
| **Proposed (lock file evidence)** | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

## Rationale

- **RHTPA 2.0.0**: incorrect -- no 2.0.x stream exists in the Version Streams configuration. PSIRT likely assigned this based on scan-time metadata. Must be removed.
- **RHTPA 2.2.0**: affected -- openssl-libs 3.0.7-25.el9_3 at tag v0.4.5 is below fix threshold 3.0.7-28.el9_4.
- **RHTPA 2.2.1**: affected -- openssl-libs 3.0.7-27.el9_4 at tag v0.4.8 is below fix threshold 3.0.7-28.el9_4.
- **RHTPA 2.2.2**: affected -- retag of 2.2.1, same openssl-libs version (3.0.7-27.el9_4).
- **RHTPA 2.2.3**: NOT affected -- openssl-libs 3.0.7-28.el9_4 at tag v0.4.11 equals fix version. Excluded.
- **RHTPA 2.2.4**: NOT affected -- openssl-libs 3.0.7-28.el9_4 at tag v0.4.12 equals fix version. Excluded.

## Proposed Jira Mutation

```
Proposed: jira.edit_issue("TC-8005", fields={
  "versions": [
    {"id": "<RHTPA-2.2.0-jira-version-id>"},
    {"id": "<RHTPA-2.2.1-jira-version-id>"},
    {"id": "<RHTPA-2.2.2-jira-version-id>"}
  ]
})
```

Version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` for the Vulnerability issue type (ID 10024) in project TC, filtered by Jira version prefix "RHTPA".

## Proposed Comment

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

RHTPA 2.0.0 was removed — no 2.0.x stream exists. Versions 2.2.3 and 2.2.4
already ship openssl-libs 3.0.7-28.el9_4 (the fix version) and are not affected.
```
