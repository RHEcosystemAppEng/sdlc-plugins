# Step 3 - Affects Versions Correction for TC-8005

## Current vs Proposed Affects Versions

**Issue stream scope**: 2.2.x (from summary suffix [rhtpa-2.2])

**Current (PSIRT-assigned)**: RHTPA 2.0.0
**Proposed (from version impact table)**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

The PSIRT-assigned version `RHTPA 2.0.0` is incorrect -- there is no 2.0.x stream
configured in the Version Streams table. The version impact analysis (using rpms.lock.yaml
data at pinned commits) shows that versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream
are affected.

Versions 2.2.3 and 2.2.4 ship openssl-libs 3.0.7-28.el9_4 (the fix version) and are
NOT affected.

## Correction

```
Current: [RHTPA 2.0.0] --> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

Scoped to stream 2.2.x per issue suffix. The 2.1.x versions (also affected) belong
to a sibling/companion CVE issue for that stream.

## Rationale

Based on rpms.lock.yaml analysis at pinned commits from the supportability matrix
in security-matrix.md. Each version's openssl-libs package version was extracted
from the lock file at the corresponding tag and compared against the fix threshold
of 3.0.7-28.el9_4.
