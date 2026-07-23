# Step 3 -- Affects Versions Correction: TC-8005

## Current vs Proposed

| | Value |
|---|---|
| Current (PSIRT-assigned) | RHTPA 2.0.0 |
| Proposed (lock file evidence) | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

## Rationale

The PSIRT-assigned Affects Version `RHTPA 2.0.0` is incorrect. There is no 2.0.x version stream configured, and lock file analysis at pinned commits from the security matrix shows the following:

- **RHTPA 2.2.0**: openssl-libs 3.0.7-25.el9_3 -- AFFECTED (below fix threshold 3.0.7-28.el9_4)
- **RHTPA 2.2.1**: openssl-libs 3.0.7-27.el9_4 -- AFFECTED (below fix threshold 3.0.7-28.el9_4)
- **RHTPA 2.2.2**: retag of 2.2.1, same openssl-libs version -- AFFECTED
- **RHTPA 2.2.3**: openssl-libs 3.0.7-28.el9_4 -- NOT AFFECTED (ships fixed version)
- **RHTPA 2.2.4**: openssl-libs 3.0.7-28.el9_4 -- NOT AFFECTED (ships fixed version)

The issue is scoped to stream 2.2.x per the summary suffix `[rhtpa-2.2]`. Only 2.2.x versions are included in the correction. Versions 2.1.0 and 2.1.1 (in the 2.1.x stream) are also affected but belong to a companion CVE issue for that stream.

## Proposed Jira Mutation

```
jira.edit_issue("TC-8005", fields={
  "versions": [
    {"id": "<RHTPA-2.2.0-version-id>"},
    {"id": "<RHTPA-2.2.1-version-id>"},
    {"id": "<RHTPA-2.2.2-version-id>"}
  ]
})
```

Version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (Step 3.1).

## Comment

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].
```
