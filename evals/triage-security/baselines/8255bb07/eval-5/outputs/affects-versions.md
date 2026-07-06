# Step 3 -- Affects Versions Correction

## Current vs Corrected Affects Versions

| Field | Value |
|-------|-------|
| Current Affects Versions (PSIRT-assigned) | RHTPA 2.0.0 |
| Corrected Affects Versions (from lock file evidence) | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

## Rationale

The PSIRT-assigned Affects Version "RHTPA 2.0.0" is incorrect. There is no 2.0.x stream configured in Version Streams, and the issue is scoped to the 2.2.x stream (from summary suffix [rhtpa-2.2]).

Lock file analysis of `rpms.lock.yaml` at each pinned tag in the 2.2.x supportability matrix shows:

| Version | openssl-libs in rpms.lock.yaml | Affected? |
|---------|-------------------------------|-----------|
| RHTPA 2.2.0 | 3.0.7-25.el9_3 | YES -- below fix threshold 3.0.7-28.el9_4 |
| RHTPA 2.2.1 | 3.0.7-27.el9_4 | YES -- below fix threshold 3.0.7-28.el9_4 |
| RHTPA 2.2.2 | (retag of 2.2.1) | YES -- same as 2.2.1 |
| RHTPA 2.2.3 | 3.0.7-28.el9_4 | NO -- equals fixed version |
| RHTPA 2.2.4 | 3.0.7-28.el9_4 | NO -- equals fixed version |

## Proposed Jira Mutation

**Action**: Remove RHTPA 2.0.0 and set Affects Versions to RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2.

This correction requires discovering the Jira version IDs dynamically via `getJiraIssueTypeMetaWithFields` for the Vulnerability issue type in project TC, then filtering by the RHTPA prefix. The version IDs would be used in the `jira.edit_issue` call to update the `versions` field.

Proposed API call (after dynamic version ID discovery):
```
jira.edit_issue(TC-8005, versions=[
  { id: "<RHTPA-2.2.0-version-id>" },
  { id: "<RHTPA-2.2.1-version-id>" },
  { id: "<RHTPA-2.2.2-version-id>" }
])
```

This update requires engineer confirmation before execution.
