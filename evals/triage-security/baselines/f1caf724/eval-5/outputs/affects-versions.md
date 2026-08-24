# Step 3 -- Affects Versions Correction

## Current vs Proposed

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

## Rationale

The PSIRT-assigned Affects Version **RHTPA 2.0.0** is incorrect. There is no
2.0.0 version in any configured version stream -- the available streams are
2.1.x and 2.2.x.

Since this issue is scoped to the **2.2.x stream** (per summary suffix
`[rhtpa-2.2]`), only 2.2.x versions are included in the correction. The
2.1.x stream versions (which are also affected) belong to a companion
sibling issue for that stream.

### Version impact evidence (rpms.lock.yaml)

| Version | openssl-libs | Affected? | Include in Affects Versions? |
|---------|--------------|-----------|------------------------------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | YES |
| 2.2.1 | 3.0.7-27.el9_4 | YES | YES |
| 2.2.2 | 3.0.7-27.el9_4 (retag) | YES | YES |
| 2.2.3 | 3.0.7-28.el9_4 | NO (fixed) | NO |
| 2.2.4 | 3.0.7-28.el9_4 | NO (fixed) | NO |

Versions 2.2.3 and 2.2.4 ship the fixed version (3.0.7-28.el9_4) and are
therefore not affected. They are excluded from Affects Versions.

## Jira Mutation (would execute after engineer confirmation)

```
jira.edit_issue("TC-8005", fields={
  "versions": [
    {"id": "<jira-id-for-RHTPA-2.2.0>"},
    {"id": "<jira-id-for-RHTPA-2.2.1>"},
    {"id": "<jira-id-for-RHTPA-2.2.2>"}
  ]
})
```

Note: Jira version IDs would be discovered dynamically via
`getJiraIssueTypeMetaWithFields` (Step 3.1). The IDs shown above are
placeholders -- the actual call uses runtime-discovered IDs, never
hardcoded values.

## Comment (would post after correction)

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

Versions 2.2.3+ ship openssl-libs 3.0.7-28.el9_4 (fixed version) and are not affected.
```
