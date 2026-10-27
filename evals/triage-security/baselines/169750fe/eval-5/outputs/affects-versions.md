# Step 3 -- Affects Versions Correction

## Current Affects Versions (PSIRT-assigned)

- RHTPA 2.0.0

## Evidence-Based Correction

PSIRT assigned **RHTPA 2.0.0** as the Affects Version, but:

1. There is no configured 2.0.x version stream in the Security Configuration. The configured streams are 2.1.x and 2.2.x.
2. This issue is scoped to the **2.2.x** stream (summary suffix `[rhtpa-2.2]`).
3. Lock file analysis of `rpms.lock.yaml` shows the following 2.2.x versions ship a vulnerable openssl-libs (before 3.0.7-28.el9_4):
   - **2.2.0** -- openssl-libs 3.0.7-25.el9_3
   - **2.2.1** -- openssl-libs 3.0.7-27.el9_4
   - **2.2.2** -- retag of 2.2.1 (same openssl-libs 3.0.7-27.el9_4)

4. Versions 2.2.3 and 2.2.4 ship openssl-libs 3.0.7-28.el9_4 (the fixed version) and are NOT affected.

## Proposed Correction

| Action | Version |
|--------|---------|
| Remove | RHTPA 2.0.0 |
| Add | RHTPA 2.2.0 |
| Add | RHTPA 2.2.1 |
| Add | RHTPA 2.2.2 |

## Rationale

RHTPA 2.0.0 is not a valid version in any configured stream and does not correspond to an actual supported product version. The correct Affects Versions are RHTPA 2.2.0, 2.2.1, and 2.2.2, which are the versions within the 2.2.x stream scope that ship openssl-libs at a version below the 3.0.7-28.el9_4 fix threshold, as confirmed by rpms.lock.yaml at each pinned build tag.
