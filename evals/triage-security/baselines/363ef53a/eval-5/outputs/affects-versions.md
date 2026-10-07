# Step 3 -- Affects Versions Correction for TC-8005

## Current vs Proposed Affects Versions

| | Affects Versions |
|---|---|
| Current (PSIRT-assigned) | RHTPA 2.0.0 |
| Proposed (lock file evidence) | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

## Rationale

- **PSIRT version is wrong**: RHTPA 2.0.0 does not correspond to any version
  in the supportability matrix or Version Streams configuration. No 2.0.x
  stream exists.
- **Issue is scoped to 2.2.x stream** (suffix `[rhtpa-2.2]`), so only
  versions from the 2.2.x stream are included.
- **Affected versions within 2.2.x**: 2.2.0 (openssl-libs 3.0.7-25.el9_3),
  2.2.1 (3.0.7-27.el9_4), and 2.2.2 (retag of 2.2.1) all ship openssl-libs
  below the fix threshold of 3.0.7-28.el9_4.
- **Not affected in 2.2.x**: 2.2.3 and 2.2.4 ship openssl-libs 3.0.7-28.el9_4
  (the fixed version), so they are excluded.
- **2.1.x versions** (2.1.0, 2.1.1) are also affected but belong to a
  different stream -- they would be tracked by a companion Vulnerability
  issue for the 2.1.x stream, not by this issue.

## Proposed Jira Update

```
jira.edit_issue("TC-8005", fields={
  "versions": [
    {"id": "<RHTPA-2.2.0-jira-id>"},
    {"id": "<RHTPA-2.2.1-jira-id>"},
    {"id": "<RHTPA-2.2.2-jira-id>"}
  ]
})
```

Version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields`
(Step 3.1). Jira version prefix filter: `RHTPA`.

## Proposed Comment

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

RHTPA 2.0.0 does not match any configured version stream -- replaced with
actual affected versions from lock file evidence.
```
