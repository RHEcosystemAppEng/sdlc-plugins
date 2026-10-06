# Step 3 -- Affects Versions Correction

## Current vs Proposed

| | Affects Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.0.0 |
| **Proposed (lock file evidence)** | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

## Rationale

The PSIRT-assigned Affects Version **RHTPA 2.0.0** is incorrect:

1. **No 2.0.x stream exists** in the configured Version Streams. The available
   streams are 2.1.x and 2.2.x. "RHTPA 2.0.0" does not correspond to any
   supported product version.

2. **This issue is scoped to the 2.2.x stream** per the summary suffix
   `[rhtpa-2.2]`. Only versions from the 2.2.x stream should appear in
   Affects Versions for this issue.

3. **Lock file analysis** at pinned commits from the supportability matrix
   shows that within the 2.2.x stream:
   - **2.2.0** (v0.4.5): openssl-libs 3.0.7-25.el9_3 -- AFFECTED
   - **2.2.1** (v0.4.8): openssl-libs 3.0.7-27.el9_4 -- AFFECTED
   - **2.2.2** (v0.4.9): openssl-libs 3.0.7-27.el9_4 -- AFFECTED (retag of 2.2.1)
   - **2.2.3** (v0.4.11): openssl-libs 3.0.7-28.el9_4 -- NOT AFFECTED (fixed)
   - **2.2.4** (v0.4.12): openssl-libs 3.0.7-28.el9_4 -- NOT AFFECTED (fixed)

4. **Versions 2.2.3 and 2.2.4 are excluded** because they ship the fixed
   version (3.0.7-28.el9_4) and are not affected by CVE-2026-40215.

## Correction Action

Update the Affects Versions field on TC-8005:

```
Current: [RHTPA 2.0.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

Post a comment documenting the correction:

> Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
> Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md.
> Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].
> RHTPA 2.0.0 does not correspond to any configured version stream.

## Cross-Stream Note

The 2.1.x stream (versions 2.1.0 and 2.1.1) is also affected by this CVE
but is tracked separately. The 2.1.x Affects Versions belong to a companion
CVE Jira for that stream (if one exists), not to this issue.
