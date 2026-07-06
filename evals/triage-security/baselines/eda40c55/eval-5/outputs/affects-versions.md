# Step 3 -- Affects Versions Correction

## Current Affects Versions (PSIRT-assigned)

- RHTPA 2.0.0

## Corrected Affects Versions (based on lock file evidence)

- RHTPA 2.2.0
- RHTPA 2.2.1
- RHTPA 2.2.2

## Rationale

The PSIRT-assigned Affects Version "RHTPA 2.0.0" is incorrect. There is no
2.0.x version stream configured in the project's Version Streams table -- the
configured streams are 2.1.x and 2.2.x.

Since the issue is scoped to the 2.2.x stream (via the `[rhtpa-2.2]` summary
suffix), the Affects Versions must reflect only the 2.2.x versions that
actually ship the vulnerable openssl-libs package:

| Version | openssl-libs version | Affected? |
|---------|---------------------|-----------|
| 2.2.0 | 3.0.7-25.el9_3 | YES -- below fix threshold 3.0.7-28.el9_4 |
| 2.2.1 | 3.0.7-27.el9_4 | YES -- below fix threshold 3.0.7-28.el9_4 |
| 2.2.2 | (retag of 2.2.1) | YES -- same as 2.2.1 |
| 2.2.3 | 3.0.7-28.el9_4 | NO -- ships fixed version |
| 2.2.4 | 3.0.7-28.el9_4 | NO -- ships fixed version |

## Proposed Jira Mutation

Remove: RHTPA 2.0.0
Add: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

This correction requires engineer confirmation before execution.
