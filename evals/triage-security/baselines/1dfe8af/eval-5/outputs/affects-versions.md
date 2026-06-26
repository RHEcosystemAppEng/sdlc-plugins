# Step 3 -- Affects Versions Correction

## Current vs Proposed

- **Current (PSIRT-assigned):** RHTPA 2.0.0
- **Proposed (lock file evidence):** RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

## Rationale

PSIRT assigned "RHTPA 2.0.0" which does not correspond to any version in
the 2.2.x stream supportability matrix. Lock file analysis at pinned commits
from security-matrix.md shows that openssl-libs is vulnerable (before
3.0.7-28.el9_4) in versions 2.2.0, 2.2.1, and 2.2.2. Versions 2.2.3 and
2.2.4 ship openssl-libs 3.0.7-28.el9_4 (the fixed version) and are not
affected.

The correction is scoped to stream 2.2.x per issue suffix `[rhtpa-2.2]`.
Affected versions from the 2.1.x stream are not included here -- they belong
to a companion issue for that stream.

## Proposed Jira Update

```
Corrected Affects Versions: [RHTPA 2.0.0] --> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].
```
