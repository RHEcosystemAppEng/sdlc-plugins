# Step 3 -- Affects Versions Correction

## Current vs Proposed

The issue is scoped to stream **2.2.x** (from summary suffix `[rhtpa-2.2]`). Only versions belonging to the 2.2.x stream are included in the Affects Versions correction.

| | Value |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.0.0 |
| **Proposed (from lock file analysis)** | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

## Rationale

- **RHTPA 2.0.0** is incorrect -- there is no 2.0.x stream in the Version Streams configuration. PSIRT assigned a non-existent version.
- **RHTPA 2.2.0** (openssl-libs 3.0.7-25.el9_3) -- AFFECTED, before fixed version 3.0.7-28.el9_4
- **RHTPA 2.2.1** (openssl-libs 3.0.7-27.el9_4) -- AFFECTED, before fixed version 3.0.7-28.el9_4
- **RHTPA 2.2.2** (retag of 2.2.1, same openssl-libs 3.0.7-27.el9_4) -- AFFECTED
- **RHTPA 2.2.3** (openssl-libs 3.0.7-28.el9_4) -- NOT affected, ships the fixed version
- **RHTPA 2.2.4** (openssl-libs 3.0.7-28.el9_4) -- NOT affected, ships the fixed version

Versions 2.1.0 and 2.1.1 (stream 2.1.x) are also affected but belong to a different stream and are outside this issue's scope. They would be tracked by a companion CVE issue for the `[rhtpa-2.1]` stream.

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

Jira version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (Step 3.1). The correction changes Affects Versions from the non-existent RHTPA 2.0.0 to the three actually-affected 2.2.x versions identified through rpms.lock.yaml analysis.

## Comment

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

RHTPA 2.0.0 does not exist in the configured Version Streams.
Versions 2.2.3 and 2.2.4 ship openssl-libs 3.0.7-28.el9_4 (the fixed version) and are not affected.
```
