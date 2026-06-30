# Step 3 -- Affects Versions Correction for TC-8005

## Current Affects Versions (PSIRT-assigned)

- RHTPA 2.0.0

## Issue

The PSIRT-assigned Affects Version "RHTPA 2.0.0" is incorrect. There is no 2.0.x
version stream configured in the project, and no RHTPA 2.0.0 appears in the
supportability matrix. The issue is scoped to the **2.2.x** stream per its summary
suffix `[rhtpa-2.2]`.

## Version Impact (2.2.x stream only, per stream scope)

Based on rpms.lock.yaml lock file analysis at pinned commits from security-matrix.md:

| Version | openssl-libs | Affected? |
|---------|--------------|-----------|
| RHTPA 2.2.0 | 3.0.7-25.el9_3 | YES |
| RHTPA 2.2.1 | 3.0.7-27.el9_4 | YES |
| RHTPA 2.2.2 | (retag of 2.2.1) | YES |
| RHTPA 2.2.3 | 3.0.7-28.el9_4 | NO (fixed) |
| RHTPA 2.2.4 | 3.0.7-28.el9_4 | NO (fixed) |

## Proposed Correction

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

The correction removes the non-existent "RHTPA 2.0.0" and replaces it with the
actually affected versions from the 2.2.x stream. Versions 2.2.3 and 2.2.4 are
excluded because they already ship the fixed openssl-libs 3.0.7-28.el9_4.

Note: The 2.1.x stream versions (2.1.0 and 2.1.1) are also affected but are NOT
included in this correction because TC-8005 is scoped to the 2.2.x stream. The
2.1.x stream should be tracked by its own companion Vulnerability issue.

## Jira Mutation (would execute after engineer confirmation)

```
jira.edit_issue("TC-8005", fields={
  "versions": [
    {"id": "<RHTPA-2.2.0-jira-version-id>"},
    {"id": "<RHTPA-2.2.1-jira-version-id>"},
    {"id": "<RHTPA-2.2.2-jira-version-id>"}
  ]
})
```

Comment to post:
```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on rpms.lock.yaml lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

RHTPA 2.0.0 does not correspond to any configured version stream. Versions
2.2.3 and 2.2.4 are not affected (ship fixed openssl-libs 3.0.7-28.el9_4).
```
