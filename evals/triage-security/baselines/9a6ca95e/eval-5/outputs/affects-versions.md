# Step 3 -- Affects Versions Correction

## Current vs. Proposed

The PSIRT-assigned Affects Versions field is incorrect. RHTPA 2.0.0 does not correspond to any version in the supportability matrix for either the 2.1.x or 2.2.x streams.

Since this issue is scoped to the **2.2.x** stream (per the `[rhtpa-2.2]` suffix), only 2.2.x versions are included in the Affects Versions correction. The 2.1.x stream is tracked by its own companion issue (if one exists) or via cross-stream preemptive remediation.

| | Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.0.0 |
| **Proposed (lock file evidence)** | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

### Rationale

- **RHTPA 2.0.0**: removed -- no such version exists in the supportability matrix. PSIRT likely assigned this based on scan-time defaults, not actual dependency analysis.
- **RHTPA 2.2.0**: added -- rpms.lock.yaml at tag v0.4.5 shows openssl-libs 3.0.7-25.el9_3, which is within the affected range (before 3.0.7-28.el9_4).
- **RHTPA 2.2.1**: added -- rpms.lock.yaml at tag v0.4.8 shows openssl-libs 3.0.7-27.el9_4, which is within the affected range.
- **RHTPA 2.2.2**: added -- retag of 2.2.1, ships the same openssl-libs 3.0.7-27.el9_4, which is within the affected range.
- **RHTPA 2.2.3**: excluded -- rpms.lock.yaml at tag v0.4.11 shows openssl-libs 3.0.7-28.el9_4, which is the fixed version (not affected).
- **RHTPA 2.2.4**: excluded -- rpms.lock.yaml at tag v0.4.12 shows openssl-libs 3.0.7-28.el9_4, which is the fixed version (not affected).

### Proposed Jira update

```
jira.edit_issue("TC-8005", fields={
  "versions": [
    {"name": "RHTPA 2.2.0"},
    {"name": "RHTPA 2.2.1"},
    {"name": "RHTPA 2.2.2"}
  ]
})
```

Note: In a live triage, Jira version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (Step 3.1) rather than using hardcoded names. The version names above are illustrative; the actual API call would use the numeric IDs from the Jira version registry.

### Comment to post

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

RHTPA 2.0.0 does not exist in the supportability matrix. Versions 2.2.3+ ship
the fixed openssl-libs 3.0.7-28.el9_4 and are not affected.
```
