# Step 3 -- Affects Versions Correction

## Current vs Proposed

- **Current Affects Versions:** RHTPA 2.0.0
- **Proposed Affects Versions:** RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

## Analysis

The PSIRT-assigned Affects Version "RHTPA 2.0.0" is **incorrect**. There is no version 2.0.0 in the supportability matrix for any configured stream. The issue is scoped to the 2.2.x stream (per the `[rhtpa-2.2]` suffix in the summary).

Based on the version impact analysis from rpms.lock.yaml data:

| Version | openssl-libs | Affected? | Include in Affects Versions? |
|---------|-------------|-----------|------------------------------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | YES |
| 2.2.1 | 3.0.7-27.el9_4 | YES | YES |
| 2.2.2 | 3.0.7-27.el9_4 (retag of 2.2.1) | YES | YES |
| 2.2.3 | 3.0.7-28.el9_4 | NO | NO |
| 2.2.4 | 3.0.7-28.el9_4 | NO | NO |

## Scope Note

This correction is scoped to the **2.2.x stream** only, per the issue's `[rhtpa-2.2]` suffix. The 2.1.x stream versions (2.1.0, 2.1.1) are also affected but belong to a companion CVE Jira for that stream -- they are NOT included in this issue's Affects Versions.

## Correction Diff

```
Current: [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

## Jira Mutation (would execute after engineer confirmation)

```
jira.edit_issue("TC-8005", fields={
  "versions": [
    {"id": "<jira-id-for-RHTPA-2.2.0>"},
    {"id": "<jira-id-for-RHTPA-2.2.1>"},
    {"id": "<jira-id-for-RHTPA-2.2.2>"}
  ]
})

jira.add_comment("TC-8005", "Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].")
```
