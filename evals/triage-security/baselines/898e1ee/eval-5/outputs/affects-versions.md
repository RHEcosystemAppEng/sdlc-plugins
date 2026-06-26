# Step 3 — Affects Versions Correction

## Current Affects Versions (PSIRT-assigned)

- RHTPA 2.0.0

## Problem

PSIRT assigned `RHTPA 2.0.0` as the Affects Version, but there is no `2.0.x` stream configured in the Version Streams table. The issue is scoped to the **2.2.x** stream (from the `[rhtpa-2.2]` suffix).

Based on the version impact analysis from Step 2, the affected 2.2.x versions are:

- **2.2.0** — ships openssl-libs 3.0.7-25.el9_3 (vulnerable)
- **2.2.1** — ships openssl-libs 3.0.7-27.el9_4 (vulnerable)
- **2.2.2** — retag of 2.2.1, same openssl-libs version (vulnerable)

The following versions are NOT affected:

- **2.2.3** — ships openssl-libs 3.0.7-28.el9_4 (fixed version)
- **2.2.4** — ships openssl-libs 3.0.7-28.el9_4 (fixed version)

## Proposed Correction

Remove:
- RHTPA 2.0.0 (no such stream exists)

Add:
- RHTPA 2.2.0
- RHTPA 2.2.1
- RHTPA 2.2.2

**Rationale**: Lock file evidence from `rpms.lock.yaml` at each pinned tag confirms that versions 2.2.0, 2.2.1, and 2.2.2 ship openssl-libs versions prior to the fix threshold (3.0.7-28.el9_4). Versions 2.2.3 and 2.2.4 ship the fixed version and are not affected.

## Jira Update

```
jira.edit_issue("TC-8005", {
  "versions": [
    { "name": "RHTPA 2.2.0" },
    { "name": "RHTPA 2.2.1" },
    { "name": "RHTPA 2.2.2" }
  ]
})
```

This update requires engineer confirmation before execution.
