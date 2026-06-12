# Step 3 -- Affects Versions Correction

## Current vs Proposed

- **Current Affects Versions (PSIRT-assigned)**: RHTPA 2.0.0
- **Proposed Affects Versions (based on lock file analysis)**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

## Rationale

The PSIRT-assigned Affects Version "RHTPA 2.0.0" is incorrect. There is no 2.0.x
stream configured in the project's Security Configuration -- the configured streams
are 2.1.x and 2.2.x.

Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md, the
affected versions within the 2.2.x stream (scoped by issue suffix `[rhtpa-2.2]`) are:

- **RHTPA 2.2.0** -- ships openssl-libs 3.0.7-25.el9_3 (vulnerable)
- **RHTPA 2.2.1** -- ships openssl-libs 3.0.7-27.el9_4 (vulnerable)
- **RHTPA 2.2.2** -- retag of 2.2.1, ships openssl-libs 3.0.7-27.el9_4 (vulnerable)

Versions 2.2.3 and 2.2.4 ship openssl-libs 3.0.7-28.el9_4 (the fixed version) and
are NOT affected.

## Proposed Jira Update

```
Current: [RHTPA 2.0.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

Scoped to stream 2.2.x per issue suffix `[rhtpa-2.2]`.

## Correction Comment

Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].
Versions 2.2.3+ ship openssl-libs 3.0.7-28.el9_4 (fixed version) and are not affected.
