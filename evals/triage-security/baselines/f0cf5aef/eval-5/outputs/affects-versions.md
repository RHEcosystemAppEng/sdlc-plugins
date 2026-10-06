# Step 3 -- Affects Versions Correction: TC-8005

## Current Affects Versions (PSIRT-assigned)

- RHTPA 2.0.0

## Problem

The PSIRT-assigned Affects Version "RHTPA 2.0.0" is incorrect:

1. There is no configured 2.0.x version stream -- the configured streams are 2.1.x and 2.2.x.
2. The issue is scoped to the 2.2.x stream (per summary suffix `[rhtpa-2.2]`).
3. Lock file analysis shows that versions 2.2.0, 2.2.1, and 2.2.2 ship vulnerable openssl-libs (before 3.0.7-28.el9_4).
4. Versions 2.2.3 and 2.2.4 ship the fixed version (3.0.7-28.el9_4) and are NOT affected.

## Proposed Correction

Remove:
- RHTPA 2.0.0

Add:
- RHTPA 2.2.0
- RHTPA 2.2.1
- RHTPA 2.2.2

The corrected Affects Versions reflect the actual lock file evidence from rpms.lock.yaml at each pinned build tag. Only versions within the issue's scoped stream (2.2.x) are included. The 2.1.x stream is also affected but is tracked separately (cross-stream impact -- see Case A in Step 8).

## Jira Update (would execute after engineer confirmation)

```
jira.edit_issue("TC-8005", {
  "versions": [
    {"name": "RHTPA 2.2.0"},
    {"name": "RHTPA 2.2.1"},
    {"name": "RHTPA 2.2.2"}
  ]
})
```

Note: Version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` rather than hardcoded. The above shows version names for clarity.
