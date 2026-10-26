# Step 3 -- Affects Versions Correction: TC-8005

## Current vs Proposed Affects Versions

| | Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.0.0 |
| **Proposed (lock file evidence)** | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

## Correction Rationale

The PSIRT-assigned Affects Version of **RHTPA 2.0.0** is incorrect:

1. **RHTPA 2.0.0 does not correspond to a version in the 2.2.x stream.** The 2.2.x
   stream covers versions 2.2.0 through 2.2.4. There is no 2.0.x stream in the
   configured Version Streams.

2. **Lock file evidence** from rpms.lock.yaml at pinned commits shows:
   - **RHTPA 2.2.0** (tag v0.4.5): openssl-libs 3.0.7-25.el9_3 -- AFFECTED (before 3.0.7-28.el9_4)
   - **RHTPA 2.2.1** (tag v0.4.8): openssl-libs 3.0.7-27.el9_4 -- AFFECTED (before 3.0.7-28.el9_4)
   - **RHTPA 2.2.2** (tag v0.4.9, retag of v0.4.8): openssl-libs 3.0.7-27.el9_4 -- AFFECTED (same as 2.2.1)
   - **RHTPA 2.2.3** (tag v0.4.11): openssl-libs 3.0.7-28.el9_4 -- NOT AFFECTED (equals fix version)
   - **RHTPA 2.2.4** (tag v0.4.12): openssl-libs 3.0.7-28.el9_4 -- NOT AFFECTED (equals fix version)

3. **Scope:** This issue is scoped to the 2.2.x stream per the summary suffix
   `[rhtpa-2.2]`. Only versions within the 2.2.x stream are included in the
   correction. The 2.1.x stream versions (2.1.0, 2.1.1) are also affected but
   belong to a companion CVE Jira for that stream (Case A cross-stream impact).

## Proposed Jira Update

```
Current: [RHTPA 2.0.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

The correction removes the non-existent RHTPA 2.0.0 and replaces it with the
three versions in the 2.2.x stream that actually ship a vulnerable version of
openssl-libs. Versions 2.2.3 and 2.2.4 are excluded because they already ship
the fixed version (3.0.7-28.el9_4).

## Jira Comment (would be posted)

> Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
> Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md.
> Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].
>
> Evidence:
> - 2.2.0 (v0.4.5): openssl-libs 3.0.7-25.el9_3 (affected)
> - 2.2.1 (v0.4.8): openssl-libs 3.0.7-27.el9_4 (affected)
> - 2.2.2 (v0.4.9): retag of 2.2.1 (affected)
> - 2.2.3 (v0.4.11): openssl-libs 3.0.7-28.el9_4 (not affected -- fixed)
> - 2.2.4 (v0.4.12): openssl-libs 3.0.7-28.el9_4 (not affected -- fixed)
