# Step 3 -- Affects Versions Correction

## Current vs Proposed

| | Value |
|---|---|
| Current (PSIRT-assigned) | RHTPA 2.0.0 |
| Proposed (lock file evidence) | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

## Rationale

The PSIRT-assigned Affects Version **RHTPA 2.0.0** is incorrect:

1. **No 2.0.x stream exists** in the configured Version Streams table. The configured
   streams are 2.1.x and 2.2.x.
2. **This issue is scoped to the 2.2.x stream** per the summary suffix `[rhtpa-2.2]`.
   Only versions belonging to the 2.2.x stream should be included in Affects Versions
   for this issue.
3. **Lock file analysis** (rpms.lock.yaml at pinned commits) shows:
   - **2.2.0** (v0.4.5): openssl-libs 3.0.7-25.el9_3 -- AFFECTED (before fix 3.0.7-28.el9_4)
   - **2.2.1** (v0.4.8): openssl-libs 3.0.7-27.el9_4 -- AFFECTED (before fix 3.0.7-28.el9_4)
   - **2.2.2** (v0.4.9): retag of v0.4.8 -- AFFECTED (same as 2.2.1)
   - **2.2.3** (v0.4.11): openssl-libs 3.0.7-28.el9_4 -- NOT affected (ships fixed version)
   - **2.2.4** (v0.4.12): openssl-libs 3.0.7-28.el9_4 -- NOT affected (ships fixed version)

## Proposed Jira Update

```
jira.edit_issue("TC-8005", fields={
  "versions": [
    {"name": "RHTPA 2.2.0"},
    {"name": "RHTPA 2.2.1"},
    {"name": "RHTPA 2.2.2"}
  ]
})
```

Correction scoped to stream 2.2.x per issue suffix. Versions 2.1.0 and 2.1.1 are
also affected but belong to a sibling CVE Jira for the 2.1.x stream (see Case A
cross-stream impact in Step 8).
