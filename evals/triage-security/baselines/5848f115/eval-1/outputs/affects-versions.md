# Step 3 -- Affects Versions Correction

## Stream Scope

This issue is **scoped** to stream **2.2.x** (from summary suffix `[rhtpa-2.2]`).

Per the scoped correction rule, only versions belonging to the 2.2.x stream are included in the Affects Versions correction for this issue. The 2.1.x stream versions (2.1.0, 2.1.1) are also affected but belong to a companion/sibling issue for that stream.

## Correction

| | Current (PSIRT-assigned) | Proposed (lock file evidence) |
|---|---|---|
| Affects Versions | RHTPA 2.0.0 | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

**PSIRT version is wrong**: "RHTPA 2.0.0" does not correspond to any version in the supportability matrix. The issue is scoped to the 2.2.x stream, and lock file analysis at pinned commits from security-matrix.md confirms that versions 2.2.0 (quinn-proto 0.11.9), 2.2.1 (quinn-proto 0.11.12), and 2.2.2 (retag of 2.2.1) all ship a vulnerable version of quinn-proto (< 0.11.14).

Versions 2.2.3 and 2.2.4 are NOT included because they ship quinn-proto 0.11.14 (the fixed version).

## Proposed Jira Update

After engineer confirmation:

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<jira-id-for-RHTPA-2.2.0>"},
    {"id": "<jira-id-for-RHTPA-2.2.1>"},
    {"id": "<jira-id-for-RHTPA-2.2.2>"}
  ]
})
```

Version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (Step 3.1).

## Comment

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].
```

## Cross-Stream Note

The 2.1.x stream (versions 2.1.0, 2.1.1) is also affected but is outside this issue's scope. Cross-stream impact is handled in Step 8 (Case A).
