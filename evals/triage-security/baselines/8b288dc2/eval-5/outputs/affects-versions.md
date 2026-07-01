# Step 3 -- Affects Versions Correction for TC-8005

## Current vs Proposed Affects Versions

The issue is scoped to stream **2.2.x** per the `[rhtpa-2.2]` suffix.

| | Affects Versions |
|---|---|
| Current (PSIRT-assigned) | RHTPA 2.0.0 |
| Proposed (lock file evidence) | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

## Rationale

PSIRT assigned `RHTPA 2.0.0` but there is no 2.0.x stream configured in Version Streams, and RHTPA 2.0.0 does not correspond to any version in the supportability matrix. This is incorrect.

Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md:

- **RHTPA 2.2.0** (tag v0.4.5): openssl-libs 3.0.7-25.el9_3 -- affected (< 3.0.7-28.el9_4)
- **RHTPA 2.2.1** (tag v0.4.8): openssl-libs 3.0.7-27.el9_4 -- affected (< 3.0.7-28.el9_4)
- **RHTPA 2.2.2** (tag v0.4.9): retag of 2.2.1 -- affected (same as 2.2.1)
- **RHTPA 2.2.3** (tag v0.4.11): openssl-libs 3.0.7-28.el9_4 -- NOT affected (= fixed version)
- **RHTPA 2.2.4** (tag v0.4.12): openssl-libs 3.0.7-28.el9_4 -- NOT affected (= fixed version)

Only versions 2.2.0, 2.2.1, and 2.2.2 are affected within the 2.2.x stream scope.

The 2.1.x versions (2.1.0, 2.1.1) are also affected but belong to a different stream -- they are tracked by their own companion CVE issue (if one exists) per the stream-scoped triage model.

## Proposed Jira Update

```
Current: [RHTPA 2.0.0] --> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

Correction scoped to stream 2.2.x per issue suffix `[rhtpa-2.2]`.

After engineer confirmation, the Affects Versions field would be updated using dynamically discovered Jira version IDs from `getJiraIssueTypeMetaWithFields`.
