# Step 3 — Affects Versions Correction

## Current vs Proposed

- **Current Affects Versions (PSIRT-assigned)**: RHTPA 2.0.0
- **Proposed Affects Versions (from lock file analysis)**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

## Rationale

The PSIRT-assigned version `RHTPA 2.0.0` is incorrect — there is no 2.0.x stream in the configured Version Streams. The issue is scoped to stream 2.2.x per the summary suffix `[rhtpa-2.2]`.

Based on lock file analysis of rpms.lock.yaml at pinned commits from the supportability matrix:

- **RHTPA 2.2.0** (tag v0.4.5): openssl-libs 3.0.7-25.el9_3 — AFFECTED (before 3.0.7-28.el9_4)
- **RHTPA 2.2.1** (tag v0.4.8): openssl-libs 3.0.7-27.el9_4 — AFFECTED (before 3.0.7-28.el9_4)
- **RHTPA 2.2.2** (tag v0.4.9): retag of 2.2.1 — AFFECTED (same as 2.2.1)
- **RHTPA 2.2.3** (tag v0.4.11): openssl-libs 3.0.7-28.el9_4 — NOT AFFECTED (meets fix threshold)
- **RHTPA 2.2.4** (tag v0.4.12): openssl-libs 3.0.7-28.el9_4 — NOT AFFECTED (meets fix threshold)

Only versions within the 2.2.x stream that are actually affected are included. Versions 2.2.3 and 2.2.4 ship the fixed version and are excluded.

## Proposed Jira Update

```
Current: [RHTPA 2.0.0] → Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

Correction scoped to stream 2.2.x per issue suffix `[rhtpa-2.2]`. The 2.1.x stream versions are affected but belong to a separate companion issue.
