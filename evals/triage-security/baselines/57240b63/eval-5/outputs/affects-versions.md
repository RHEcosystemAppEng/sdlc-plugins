# Step 3 -- Affects Versions Correction: TC-8005

## Current vs Proposed

| | Value |
|---|---|
| Current Affects Versions | RHTPA 2.0.0 |
| Proposed Affects Versions | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

## Rationale

The PSIRT-assigned Affects Version "RHTPA 2.0.0" is incorrect. There is no version 2.0.0 in any configured version stream. The issue is scoped to the 2.2.x stream (per summary suffix `[rhtpa-2.2]`), so only versions within that stream are included.

Based on lock file analysis of `rpms.lock.yaml` at pinned commits from the supportability matrix:

- **RHTPA 2.2.0** (build v0.4.5): ships openssl-libs 3.0.7-25.el9_3 -- AFFECTED
- **RHTPA 2.2.1** (build v0.4.8): ships openssl-libs 3.0.7-27.el9_4 -- AFFECTED
- **RHTPA 2.2.2** (build v0.4.9): retag of 2.2.1 (same source as v0.4.8) -- AFFECTED
- **RHTPA 2.2.3** (build v0.4.11): ships openssl-libs 3.0.7-28.el9_4 -- NOT AFFECTED (fixed version)
- **RHTPA 2.2.4** (build v0.4.12): ships openssl-libs 3.0.7-28.el9_4 -- NOT AFFECTED (fixed version)

Versions 2.2.3 and 2.2.4 ship the fixed version (3.0.7-28.el9_4) and are excluded from Affects Versions.

Note: The 2.1.x stream versions (2.1.0, 2.1.1) are also affected but belong to a different stream scope. They are not included in this issue's Affects Versions. They should be tracked by a companion CVE Jira for the 2.1.x stream.

## PROPOSAL: Jira Mutation

```
jira.edit_issue("TC-8005", fields={
  "versions": [
    {"id": "<RHTPA-2.2.0-jira-id>"},
    {"id": "<RHTPA-2.2.1-jira-id>"},
    {"id": "<RHTPA-2.2.2-jira-id>"}
  ]
})
```

Jira version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (Step 3.1). The IDs shown above are placeholders pending dynamic discovery.

## PROPOSAL: Jira Comment

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

Versions 2.2.3+ ship the fixed openssl-libs 3.0.7-28.el9_4 and are not affected.
```
