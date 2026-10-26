# Step 3 -- Affects Versions Correction

## Current vs Proposed Affects Versions

The issue TC-8001 is scoped to stream **2.2.x** (from summary suffix `[rhtpa-2.2]`).
Per the scoping rules, only versions belonging to the 2.2.x stream are included in
the Affects Versions correction for this issue. The 2.1.x versions (also affected)
belong to a sibling issue or would be handled via cross-stream preemptive remediation.

### Correction

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

### Rationale

- **RHTPA 2.0.0** (current): Incorrect. There is no 2.0.x version stream configured
  in Security Configuration. PSIRT assigned this version based on scan time, not actual
  dependency analysis. This version does not exist in the supportability matrix.
- **RHTPA 2.2.0**: Affected. Ships quinn-proto 0.11.9 (< 0.11.14 fix threshold).
  Source: `git show v0.4.5:Cargo.lock`.
- **RHTPA 2.2.1**: Affected. Ships quinn-proto 0.11.12 (< 0.11.14 fix threshold).
  Source: `git show v0.4.8:Cargo.lock`.
- **RHTPA 2.2.2**: Affected. Retag of 2.2.1 -- ships same quinn-proto 0.11.12.
- **RHTPA 2.2.3**: NOT affected. Ships quinn-proto 0.11.14 (= fix threshold). Excluded.
- **RHTPA 2.2.4**: NOT affected. Ships quinn-proto 0.11.14 (= fix threshold). Excluded.

### Jira Version Discovery

Jira versions matching prefix "RHTPA" would be discovered dynamically via
`getJiraIssueTypeMetaWithFields` for the Vulnerability issue type (ID: 10024).
The version IDs for RHTPA 2.2.0, RHTPA 2.2.1, and RHTPA 2.2.2 would be extracted
from the `allowedValues` array to construct the update.

### Planned Jira Operation (not performed)

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<RHTPA-2.2.0-version-id>"},
    {"id": "<RHTPA-2.2.1-version-id>"},
    {"id": "<RHTPA-2.2.2-version-id>"}
  ]
})
```

A correction comment would be posted to TC-8001 documenting the change:
"Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2]."

No Jira operations were actually performed.
