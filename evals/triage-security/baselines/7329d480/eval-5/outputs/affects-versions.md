# Step 3 -- Affects Versions Correction

## Current Affects Versions (PSIRT-assigned)

- RHTPA 2.0.0

## Issues with current Affects Versions

1. **RHTPA 2.0.0 is not in any configured version stream.** The configured
   streams are 2.1.x and 2.2.x. There is no 2.0.x stream in the Version
   Streams table. RHTPA 2.0.0 does not correspond to any version in the
   supportability matrix.
2. **The issue is scoped to the 2.2.x stream** (summary suffix `[rhtpa-2.2]`).
   Only 2.2.x versions should appear in Affects Versions for this issue.
3. **Lock file evidence shows versions 2.2.0, 2.2.1, and 2.2.2 are affected.**
   Versions 2.2.3 and 2.2.4 ship the fixed openssl-libs (3.0.7-28.el9_4) and
   are NOT affected.

## Corrected Affects Versions

**Remove:**
- RHTPA 2.0.0 (not in any supported stream; no lock file evidence)

**Add:**
- RHTPA 2.2.0 (openssl-libs 3.0.7-25.el9_3 -- vulnerable)
- RHTPA 2.2.1 (openssl-libs 3.0.7-27.el9_4 -- vulnerable)
- RHTPA 2.2.2 (retag of 2.2.1; openssl-libs 3.0.7-27.el9_4 -- vulnerable)

**Final Affects Versions:**
- RHTPA 2.2.0
- RHTPA 2.2.1
- RHTPA 2.2.2

## Rationale

PSIRT assigned RHTPA 2.0.0 based on scan-time data, but no 2.0.x stream
exists in the project configuration. Lock file analysis of rpms.lock.yaml
at each pinned build tag in the 2.2.x supportability matrix confirms that
openssl-libs was updated to the fixed version (3.0.7-28.el9_4) starting
with version 2.2.3 (build tag v0.4.11). Versions 2.2.0 through 2.2.2
shipped vulnerable versions and are the correct Affects Versions for this
stream-scoped issue.
