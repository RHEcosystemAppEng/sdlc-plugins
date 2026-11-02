# Step 3 — Affects Versions Correction

## 3.1 — Discover Available Jira Versions

Proposed call: `jira.getJiraIssueTypeMetaWithFields(projectIdOrKey: "TC", issueTypeId: "10024")`

The versions are discovered dynamically from the Jira API (Important Rule 6 — never hardcode Jira version IDs). Version names matching the Jira version prefix "RHTPA" are used.

## 3.2 — Compare and Correct Affects Versions

### Stream Scope

This issue is scoped to the **2.2.x** stream (suffix `[rhtpa-2.2]`). The Affects Versions correction only includes versions belonging to the 2.2.x stream.

### Version Impact (2.2.x stream only)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.2.0 | 0.11.9 | YES |
| 2.2.1 | 0.11.12 | YES |
| 2.2.2 | 0.11.12 | YES (retag of 2.2.1) |
| 2.2.3 | 0.11.14 | NO |
| 2.2.4 | 0.11.14 | NO |

### Proposed Correction

The PSIRT-assigned Affects Versions are incorrect:

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

**Diff**: RHTPA 2.0.0 does not match any version in the supportability matrix — it appears to be an erroneous assignment. The lock-file-verified affected versions for the 2.2.x stream are RHTPA 2.2.0, RHTPA 2.2.1, and RHTPA 2.2.2.

Version names are referenced from the supportability matrix (Important Rule 6): RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2. The Jira version IDs would be resolved dynamically via `getJiraIssueTypeMetaWithFields` at runtime.

### Proposed Jira Mutation (pending engineer confirmation)

```
jira.edit_issue(TC-8001, fields={
  "versions": [{"id": "<jira-id-for-RHTPA-2.2.0>"}, {"id": "<jira-id-for-RHTPA-2.2.1>"}, {"id": "<jira-id-for-RHTPA-2.2.2>"}]
})
```

### Proposed Comment

```
jira.add_comment(TC-8001,
  "Corrected Affects Versions: [RHTPA 2.0.0] → [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
  Based on lock file analysis at pinned commits from security-matrix.md.
  Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

  [Comment Footnote]")
```

Note: The 2.1.x stream versions (2.1.0, 2.1.1) are also affected but belong to a different stream — they would be handled by a companion issue for that stream (see Step 4 sibling check).
