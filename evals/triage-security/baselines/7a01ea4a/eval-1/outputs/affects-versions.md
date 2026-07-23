# Step 3 -- Affects Versions Correction

## Current vs Proposed Affects Versions

The issue TC-8001 is **scoped to stream 2.2.x** (from summary suffix `[rhtpa-2.2]`).
The Affects Versions correction is scoped to only include versions from that stream.

### PSIRT-Assigned (Current)

- RHTPA 2.0.0

### Lock-File Evidence (Proposed)

Based on the version impact table, the following 2.2.x versions are affected
(quinn-proto < 0.11.14):

- **RHTPA 2.2.0** -- ships quinn-proto 0.11.9 (affected)
- **RHTPA 2.2.1** -- ships quinn-proto 0.11.12 (affected)
- **RHTPA 2.2.2** -- retag of 2.2.1, ships quinn-proto 0.11.12 (affected)

Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (the fixed version) and are
**not affected**.

### Correction

```
Current: [RHTPA 2.0.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

**Rationale**: RHTPA 2.0.0 does not exist in the supportability matrix or as a
configured version stream. The PSIRT-assigned version is incorrect. Lock file
analysis at pinned commits from security-matrix.md confirms that versions 2.2.0,
2.2.1, and 2.2.2 within the issue's scoped stream (2.2.x) ship vulnerable
versions of quinn-proto.

### Jira Mutation (requires confirmation)

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<RHTPA-2.2.0-jira-version-id>"},
    {"id": "<RHTPA-2.2.1-jira-version-id>"},
    {"id": "<RHTPA-2.2.2-jira-version-id>"}
  ]
})
```

Version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields`.

### Comment

```
jira.add_comment("TC-8001",
  "Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
  Based on lock file analysis at pinned commits from security-matrix.md.
  Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].
  RHTPA 2.0.0 does not exist in the supportability matrix.
  Versions 2.2.3+ ship quinn-proto 0.11.14 (fixed) and are not affected.")
```

## Cross-Stream Note

The 2.1.x stream is also affected (versions 2.1.0 and 2.1.1 both ship
quinn-proto 0.11.9), but those versions are **not** included in this issue's
Affects Versions because TC-8001 is scoped to stream 2.2.x. The 2.1.x impact
is addressed via Case B cross-stream remediation in Step 8.
