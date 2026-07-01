# Step 3 — Affects Versions Correction for TC-8005

## Current vs Proposed Affects Versions

The PSIRT-assigned Affects Versions do not match the lock file evidence. The issue is scoped to stream 2.2.x.

| | Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.0.0 |
| **Proposed (lock-file-verified)** | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

**Diff**: `Current: [RHTPA 2.0.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

### Rationale

- **RHTPA 2.0.0** is being removed — there is no 2.0.x stream configured in the Version Streams table, and the issue is scoped to the 2.2.x stream via its `[rhtpa-2.2]` suffix.
- **RHTPA 2.2.0** (openssl-libs 3.0.7-25.el9_3) — affected, ships vulnerable version
- **RHTPA 2.2.1** (openssl-libs 3.0.7-27.el9_4) — affected, ships vulnerable version
- **RHTPA 2.2.2** (retag of 2.2.1) — affected, same openssl-libs as 2.2.1
- **RHTPA 2.2.3** (openssl-libs 3.0.7-28.el9_4) — NOT affected, ships the fix
- **RHTPA 2.2.4** (openssl-libs 3.0.7-28.el9_4) — NOT affected, ships the fix

Version names are drawn from the Jira version prefix (RHTPA) combined with version numbers from the supportability matrix — not hardcoded Jira version IDs.

### Proposed Action

Update Affects Versions on TC-8005 using dynamically discovered Jira version IDs from `getJiraIssueTypeMetaWithFields`:

```
jira.edit_issue("TC-8005", fields={
  "versions": [{"id": "<RHTPA-2.2.0-id>"}, {"id": "<RHTPA-2.2.1-id>"}, {"id": "<RHTPA-2.2.2-id>"}]
})
```

Post a comment documenting the correction:

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].
```

This is a proposed action awaiting engineer confirmation before execution.
