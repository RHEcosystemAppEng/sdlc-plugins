# Step 3 -- Affects Versions Correction

## Current vs Proposed Affects Versions

The issue TC-8001 is **scoped to stream 2.2.x** (per the `[rhtpa-2.2]` suffix). Only versions belonging to stream 2.2.x are included in the Affects Versions correction, even though stream 2.1.x is also affected (2.1.x versions are tracked by companion/sibling issues per the PSIRT per-stream model).

### Correction

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

### Rationale

- **RHTPA 2.0.0** (current) -- incorrect. No 2.0.x version stream exists in the configured Version Streams. PSIRT assigned this version incorrectly.
- **RHTPA 2.2.0** -- affected. Ships quinn-proto 0.11.9 (< 0.11.14). Confirmed via `git show v0.4.5:Cargo.lock`.
- **RHTPA 2.2.1** -- affected. Ships quinn-proto 0.11.12 (< 0.11.14). Confirmed via `git show v0.4.8:Cargo.lock`.
- **RHTPA 2.2.2** -- affected. Retag of 2.2.1, same quinn-proto 0.11.12. Confirmed via retag relationship in supportability matrix.
- **RHTPA 2.2.3** -- NOT affected. Ships quinn-proto 0.11.14 (fixed version). Excluded from Affects Versions.
- **RHTPA 2.2.4** -- NOT affected. Ships quinn-proto 0.11.14 (fixed version). Excluded from Affects Versions.

### Proposed Jira Mutation

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<jira-id-for-RHTPA-2.2.0>"},
    {"id": "<jira-id-for-RHTPA-2.2.1>"},
    {"id": "<jira-id-for-RHTPA-2.2.2>"}
  ]
})
```

Version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (Step 3.1) -- not hardcoded.

### Proposed Comment

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].
RHTPA 2.0.0 does not correspond to any configured version stream and has been removed.
RHTPA 2.2.3 and RHTPA 2.2.4 ship quinn-proto 0.11.14 (fixed version) and are excluded.
```

## Cross-Stream Impact Note

Although this Affects Versions correction is scoped to stream 2.2.x, the version impact analysis shows that stream **2.1.x** (versions 2.1.0 and 2.1.1) is also affected. This is handled via Case A (cross-stream impact) in Step 8, not by adding 2.1.x versions to this issue's Affects Versions.
