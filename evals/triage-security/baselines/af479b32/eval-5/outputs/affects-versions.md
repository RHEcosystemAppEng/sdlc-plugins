# Step 3 -- Affects Versions Correction

## Current vs Proposed Affects Versions

The issue is scoped to the **2.2.x** stream (from suffix `[rhtpa-2.2]`). Only versions within this stream are included in the correction.

### PSIRT-Assigned (Current)

| Affects Versions |
|------------------|
| RHTPA 2.0.0 |

### Lock File Evidence (Proposed)

Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md:

| Version | openssl-libs | Affected? | Include in Affects Versions? |
|---------|-------------|-----------|-------------------------------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | YES |
| 2.2.1 | 3.0.7-27.el9_4 | YES | YES |
| 2.2.2 | 3.0.7-27.el9_4 | YES | YES (retag of 2.2.1) |
| 2.2.3 | 3.0.7-28.el9_4 | NO | NO (ships fixed version) |
| 2.2.4 | 3.0.7-28.el9_4 | NO | NO (ships fixed version) |

### Correction

```
Current: [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

**Rationale**: PSIRT assigned RHTPA 2.0.0, which does not exist in the supportability matrix or Jira version registry for this product. The actual affected versions in the 2.2.x stream are 2.2.0, 2.2.1, and 2.2.2, which ship openssl-libs versions prior to the fix threshold (3.0.7-28.el9_4). Versions 2.2.3 and 2.2.4 already ship the fixed version and are excluded.

### Jira Mutation (requires engineer confirmation)

```
jira.edit_issue("TC-8005", fields={
  "versions": [
    {"id": "<RHTPA-2.2.0-version-id>"},
    {"id": "<RHTPA-2.2.1-version-id>"},
    {"id": "<RHTPA-2.2.2-version-id>"}
  ]
})
```

Version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (Step 3.1).

### Comment to Post

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

RHTPA 2.0.0 does not exist in the supportability matrix. Versions 2.2.0-2.2.2
ship openssl-libs < 3.0.7-28.el9_4 (vulnerable). Versions 2.2.3+ ship the
fixed version.
```
