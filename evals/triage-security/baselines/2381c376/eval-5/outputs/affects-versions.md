# Step 3 -- Affects Versions Correction

## Current vs Proposed

The issue is scoped to the **2.2.x** stream per the `[rhtpa-2.2]` summary suffix. Only versions belonging to the 2.2.x stream are included in the correction.

| | Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.0.0 |
| **Proposed (lock file evidence)** | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

## Correction Rationale

- **RHTPA 2.0.0** is incorrect -- no `2.0.x` version stream exists in the configured Version Streams table. PSIRT likely assigned this version based on scan time rather than dependency analysis.
- **RHTPA 2.2.0** (build v0.4.5): ships openssl-libs 3.0.7-25.el9_3, which is before the fix threshold 3.0.7-28.el9_4. **Affected.**
- **RHTPA 2.2.1** (build v0.4.8): ships openssl-libs 3.0.7-27.el9_4, which is before the fix threshold. **Affected.**
- **RHTPA 2.2.2** (build v0.4.9): retag of 2.2.1, same openssl-libs version. **Affected.**
- **RHTPA 2.2.3** (build v0.4.11): ships openssl-libs 3.0.7-28.el9_4, which equals the fixed version. **Not affected.**
- **RHTPA 2.2.4** (build v0.4.12): ships openssl-libs 3.0.7-28.el9_4. **Not affected.**

## Versions Not Included (Cross-Stream)

The following versions are affected but belong to the **2.1.x** stream, which is outside this issue's scope:

- RHTPA 2.1.0 (openssl-libs 3.0.7-24.el9) -- affected, tracked via cross-stream Case A
- RHTPA 2.1.1 (openssl-libs 3.0.7-24.el9) -- affected, tracked via cross-stream Case A

These versions would be covered by a sibling CVE Jira for the 2.1.x stream (if one exists) or by preemptive remediation tasks created in Step 8 Case A.

## Proposed Jira Mutation (not executed)

```
jira.edit_issue("TC-8005", fields={
  "versions": [
    {"id": "<jira-id-for-RHTPA-2.2.0>"},
    {"id": "<jira-id-for-RHTPA-2.2.1>"},
    {"id": "<jira-id-for-RHTPA-2.2.2>"}
  ]
})
```

Jira version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` at runtime (Step 3.1). Hardcoded IDs are not used.

## Proposed Jira Comment (not executed)

```
Corrected Affects Versions: [RHTPA 2.0.0] --> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

RHTPA 2.0.0 does not correspond to any configured version stream.
Versions 2.2.3+ already ship the fixed openssl-libs 3.0.7-28.el9_4.
```
