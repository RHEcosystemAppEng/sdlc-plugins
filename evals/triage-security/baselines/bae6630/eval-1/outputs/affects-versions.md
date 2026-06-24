# Step 3 -- Affects Versions Correction

## Current vs Proposed Affects Versions

The issue TC-8001 is **scoped to stream 2.2.x** (per summary suffix `[rhtpa-2.2]`).

### PSIRT-Assigned (Current)

| Affects Version |
|-----------------|
| RHTPA 2.0.0 |

### Version Impact (2.2.x stream only, per stream scope)

From the version impact table, the affected versions within the 2.2.x stream are:

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.2.0 | 0.11.9 | YES |
| 2.2.1 | 0.11.12 | YES |
| 2.2.2 | 0.11.12 | YES (retag of 2.2.1) |
| 2.2.3 | 0.11.14 | NO |
| 2.2.4 | 0.11.14 | NO |

### Correction

The PSIRT-assigned Affects Version "RHTPA 2.0.0" is **incorrect** -- there is no 2.0.x stream configured, and no RHTPA 2.0.0 version exists in the supportability matrix. The issue is scoped to stream 2.2.x per the summary suffix `[rhtpa-2.2]`.

**Current:** `[RHTPA 2.0.0]`
**Proposed:** `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

### Rationale

- **RHTPA 2.0.0 removed**: This version does not exist in any configured version stream. PSIRT likely assigned it in error.
- **RHTPA 2.2.0 added**: Ships quinn-proto 0.11.9, which is within the vulnerable range (< 0.11.14).
- **RHTPA 2.2.1 added**: Ships quinn-proto 0.11.12, which is within the vulnerable range (< 0.11.14).
- **RHTPA 2.2.2 added**: Retag of 2.2.1, ships the same quinn-proto 0.11.12, which is within the vulnerable range.
- **RHTPA 2.2.3 excluded**: Ships quinn-proto 0.11.14 (the fixed version) -- not affected.
- **RHTPA 2.2.4 excluded**: Ships quinn-proto 0.11.14 (the fixed version) -- not affected.

Versions 2.1.0 and 2.1.1 are also affected but belong to the 2.1.x stream, which is outside this issue's scope. Cross-stream impact is handled via Case B (cross-stream impact notice and preemptive remediation tasks for the 2.1.x stream).

### Jira Mutation (proposed)

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<RHTPA-2.2.0-jira-id>"},
    {"id": "<RHTPA-2.2.1-jira-id>"},
    {"id": "<RHTPA-2.2.2-jira-id>"}
  ]
})
```

Comment to add:
```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

RHTPA 2.0.0 does not exist in any configured version stream.
RHTPA 2.2.0 ships quinn-proto 0.11.9 (vulnerable, < 0.11.14).
RHTPA 2.2.1 ships quinn-proto 0.11.12 (vulnerable, < 0.11.14).
RHTPA 2.2.2 is a retag of 2.2.1, same quinn-proto 0.11.12 (vulnerable).
RHTPA 2.2.3+ ships quinn-proto 0.11.14 (fixed version, not affected).
```
