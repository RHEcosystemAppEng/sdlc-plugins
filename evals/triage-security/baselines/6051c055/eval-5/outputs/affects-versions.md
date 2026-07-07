# Step 3 -- Affects Versions Correction

## Current Affects Versions (PSIRT-assigned)

- RHTPA 2.0.0

## Corrected Affects Versions (based on lock file evidence)

The issue is scoped to the **2.2.x** stream. Based on rpms.lock.yaml analysis,
the following versions within that stream ship a vulnerable openssl-libs
(before 3.0.7-28.el9_4):

- **RHTPA 2.2.0** -- openssl-libs 3.0.7-25.el9_3 (affected)
- **RHTPA 2.2.1** -- openssl-libs 3.0.7-27.el9_4 (affected)
- **RHTPA 2.2.2** -- openssl-libs 3.0.7-27.el9_4 (affected, retag of 2.2.1)

## Correction Required

| Action | Version | Reason |
|--------|---------|--------|
| REMOVE | RHTPA 2.0.0 | No 2.0.x stream configured; does not exist in Version Streams table. PSIRT-assigned version is incorrect. |
| ADD | RHTPA 2.2.0 | rpms.lock.yaml at v0.4.5 shows openssl-libs 3.0.7-25.el9_3 (vulnerable) |
| ADD | RHTPA 2.2.1 | rpms.lock.yaml at v0.4.8 shows openssl-libs 3.0.7-27.el9_4 (vulnerable) |
| ADD | RHTPA 2.2.2 | retag of 2.2.1; same openssl-libs 3.0.7-27.el9_4 (vulnerable) |

Versions 2.2.3 and 2.2.4 are NOT added because they ship openssl-libs 3.0.7-28.el9_4
(the fixed version).

## Cross-Stream Note

The 2.1.x stream (versions 2.1.0 and 2.1.1) is also affected (openssl-libs
3.0.7-24.el9), but this issue is scoped to the 2.2.x stream. Cross-stream
impact is handled via Case B (cross-stream impact comment on TC-8005).
