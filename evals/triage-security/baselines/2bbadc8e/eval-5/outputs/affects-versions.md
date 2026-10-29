# Step 3 -- Affects Versions Correction

## 3.1 -- Available Jira Versions

PROPOSAL: Query Jira for available versions matching prefix "RHTPA" via
`getJiraIssueTypeMetaWithFields` (project: TC, issue type: 10024).

Expected matching versions (based on the 2.2.x supportability matrix):

| Jira ID | Name | Released | Release Date |
|---------|------|----------|--------------|
| (dynamic) | RHTPA 2.2.0 | yes | 2025-12-03 |
| (dynamic) | RHTPA 2.2.1 | yes | 2026-02-05 |
| (dynamic) | RHTPA 2.2.2 | yes | 2026-02-23 |
| (dynamic) | RHTPA 2.2.3 | yes | 2026-03-23 |
| (dynamic) | RHTPA 2.2.4 | yes | 2026-05-04 |

Note: Jira version IDs are discovered dynamically at runtime, not hardcoded.

## 3.2 -- Comparison and Correction

**Stream scope**: This issue is scoped to the **2.2.x** stream (from summary
suffix `[rhtpa-2.2]`). Only versions belonging to the 2.2.x stream are
included in the Affects Versions correction.

**Version impact (2.2.x stream only)**:

| Version | Affected? |
|---------|-----------|
| RHTPA 2.2.0 | YES |
| RHTPA 2.2.1 | YES |
| RHTPA 2.2.2 | YES (retag of 2.2.1) |
| RHTPA 2.2.3 | NO (ships fixed 3.0.7-28.el9_4) |
| RHTPA 2.2.4 | NO (ships fixed 3.0.7-28.el9_4) |

### Proposed Correction

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

**Rationale**: The PSIRT-assigned Affects Version "RHTPA 2.0.0" is incorrect --
there is no 2.0.x version stream configured. Lock file analysis at pinned
commits from the supportability matrix confirms that openssl-libs versions
before 3.0.7-28.el9_4 are shipped in versions 2.2.0, 2.2.1, and 2.2.2.
Versions 2.2.3 and 2.2.4 ship the fixed version and are excluded.

### PROPOSAL: Jira Mutation

After engineer confirmation, the following mutation would be executed:

```
jira.edit_issue("TC-8005", fields={
  "versions": [
    {"id": "<RHTPA-2.2.0-jira-id>"},
    {"id": "<RHTPA-2.2.1-jira-id>"},
    {"id": "<RHTPA-2.2.2-jira-id>"}
  ]
})
```

### PROPOSAL: Correction Comment

```
jira.add_comment("TC-8005",
  "Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
   Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md.
   Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

   Evidence:
   - v0.4.5 (2.2.0): openssl-libs 3.0.7-25.el9_3 (affected)
   - v0.4.8 (2.2.1): openssl-libs 3.0.7-27.el9_4 (affected)
   - v0.4.9 (2.2.2): retag of 2.2.1 (affected)
   - v0.4.11 (2.2.3): openssl-libs 3.0.7-28.el9_4 (fixed)
   - v0.4.12 (2.2.4): openssl-libs 3.0.7-28.el9_4 (fixed)

   [Comment Footnote]")
```
