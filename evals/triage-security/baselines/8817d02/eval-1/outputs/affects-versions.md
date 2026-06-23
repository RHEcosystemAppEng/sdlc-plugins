# Step 3 -- Affects Versions Correction

## 3.1 -- Available Jira Versions

PROPOSED: Discover available Jira versions via `getJiraIssueTypeMetaWithFields`:

```
jira.getJiraIssueTypeMetaWithFields(
  projectIdOrKey: "TC",
  issueTypeId: "10024"
)
```

From the `versions` field `allowedValues`, filter by Jira version prefix `RHTPA`. Expected registry (based on the supportability matrix versions):

| Jira ID | Name | Released | Release Date |
|---------|------|----------|--------------|
| (dynamic) | RHTPA 2.1.0 | yes | 2025-09-15 |
| (dynamic) | RHTPA 2.1.1 | yes | 2025-11-20 |
| (dynamic) | RHTPA 2.2.0 | yes | 2025-12-03 |
| (dynamic) | RHTPA 2.2.1 | yes | 2026-02-05 |
| (dynamic) | RHTPA 2.2.2 | yes | 2026-02-23 |
| (dynamic) | RHTPA 2.2.3 | yes | 2026-03-23 |
| (dynamic) | RHTPA 2.2.4 | yes | 2026-05-04 |

## 3.2 -- Compare and Correct Affects Versions

### Current State

- **Current Affects Versions (PSIRT-assigned)**: `RHTPA 2.0.0`
- **Issue stream scope**: `2.2.x` (from summary suffix `[rhtpa-2.2]`)

### Analysis

The PSIRT-assigned version `RHTPA 2.0.0` is **wrong**. There is no 2.0.x stream configured in the Version Streams table, and `RHTPA 2.0.0` does not appear in the supportability matrix. PSIRT likely assigned this version based on scan-time metadata rather than actual dependency analysis.

### Stream-Scoped Impact

Since TC-8001 is scoped to the **2.2.x** stream, only 2.2.x versions are included in the Affects Versions correction (per Step 3.2 scoping rules). The 2.1.x versions, while also affected, belong to a different stream and would be tracked by a sibling or companion issue.

From the version impact table, the affected 2.2.x versions are:

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.2.0 | 0.11.9 | YES |
| 2.2.1 | 0.11.12 | YES |
| 2.2.2 | (retag of 2.2.1) | YES |
| 2.2.3 | 0.11.14 | NO |
| 2.2.4 | 0.11.14 | NO |

### Proposed Correction

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

The correction:
- **Removes** `RHTPA 2.0.0` (does not exist as a valid version; no 2.0.x stream)
- **Adds** `RHTPA 2.2.0` (quinn-proto 0.11.9 -- affected)
- **Adds** `RHTPA 2.2.1` (quinn-proto 0.11.12 -- affected)
- **Adds** `RHTPA 2.2.2` (retag of 2.2.1, same quinn-proto 0.11.12 -- affected)
- **Excludes** `RHTPA 2.2.3` and `RHTPA 2.2.4` (quinn-proto 0.11.14 -- already fixed)

### PROPOSED Jira Mutation (requires engineer confirmation)

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<RHTPA-2.2.0-jira-id>"},
    {"id": "<RHTPA-2.2.1-jira-id>"},
    {"id": "<RHTPA-2.2.2-jira-id>"}
  ]
})
```

(Jira version IDs would be resolved dynamically from Step 3.1 discovery.)

### PROPOSED Comment

```
jira.add_comment("TC-8001", "Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

Evidence:
- RHTPA 2.2.0 (v0.4.5): quinn-proto 0.11.9 -- affected (< 0.11.14)
- RHTPA 2.2.1 (v0.4.8): quinn-proto 0.11.12 -- affected (< 0.11.14)
- RHTPA 2.2.2 (v0.4.9): retag of 2.2.1 -- affected (same as 2.2.1)
- RHTPA 2.2.3 (v0.4.11): quinn-proto 0.11.14 -- NOT affected (fixed version)
- RHTPA 2.2.4 (v0.4.12): quinn-proto 0.11.14 -- NOT affected (fixed version)

RHTPA 2.0.0 was removed -- no 2.0.x stream exists in the supportability matrix.")
```
