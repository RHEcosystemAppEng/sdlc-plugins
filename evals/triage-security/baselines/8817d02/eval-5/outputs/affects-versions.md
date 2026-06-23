# Step 3 -- Affects Versions Correction

## 3.1 -- Current Affects Versions

The PSIRT-assigned Affects Versions on TC-8005: **RHTPA 2.0.0**

## 3.2 -- Version Impact Evidence (scoped to 2.2.x stream)

From lock file analysis at pinned commits in the 2.2.x stream's supportability matrix:

| Version | openssl-libs | Affected? |
|---------|-------------|-----------|
| 2.2.0 | 3.0.7-25.el9_3 | YES |
| 2.2.1 | 3.0.7-27.el9_4 | YES |
| 2.2.2 | (retag of 2.2.1) | YES |
| 2.2.3 | 3.0.7-28.el9_4 | NO |
| 2.2.4 | 3.0.7-28.el9_4 | NO |

## 3.3 -- PSIRT Version is Wrong

The PSIRT-assigned version **RHTPA 2.0.0** does not correspond to any existing version in the 2.2.x stream. There is no 2.0.x stream configured in the Version Streams table at all. This is an incorrect PSIRT assignment.

The affected versions within the scoped 2.2.x stream are: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2.

Versions 2.2.3 and 2.2.4 already ship the fixed openssl-libs (3.0.7-28.el9_4) and are NOT affected.

## PROPOSED Correction

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

**Rationale**: RHTPA 2.0.0 does not exist in any configured stream. Lock file analysis at the 2.2.x stream's pinned commits confirms that versions 2.2.0, 2.2.1, and 2.2.2 ship openssl-libs < 3.0.7-28.el9_4 (the fix threshold). Versions 2.2.3+ already include the fix.

Scoped to stream 2.2.x per issue suffix `[rhtpa-2.2]`.

### PROPOSED Jira Mutation

```
jira.edit_issue("TC-8005", fields={
  "versions": [
    {"id": "<jira-id-for-RHTPA-2.2.0>"},
    {"id": "<jira-id-for-RHTPA-2.2.1>"},
    {"id": "<jira-id-for-RHTPA-2.2.2>"}
  ]
})
```

Note: Jira version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` in a live triage. The IDs shown here are placeholders.

### PROPOSED Comment

```
jira.add_comment("TC-8005", "Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

Versions 2.2.3 and 2.2.4 ship openssl-libs 3.0.7-28.el9_4 (the fixed version) and are not affected.")
```
