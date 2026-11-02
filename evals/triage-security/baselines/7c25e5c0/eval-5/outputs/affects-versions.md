# Step 3 — Affects Versions Correction

## Current vs Proposed Affects Versions

The issue is scoped to the **2.2.x** stream. Only versions from this stream are included in the correction.

**Current Affects Versions** (PSIRT-assigned): `[RHTPA 2.0.0]`
**Proposed Affects Versions** (lock-file-verified): `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

### Correction Details

| Action | Versions |
|--------|----------|
| Remove | RHTPA 2.0.0 (not a valid version in any configured stream) |
| Add | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

The PSIRT-assigned version "RHTPA 2.0.0" does not correspond to any supported version in the configured Version Streams. The lock-file-verified affected versions are RHTPA 2.2.0, 2.2.1, and 2.2.2 — these are the versions that ship openssl-libs < 3.0.7-28.el9_4.

Versions RHTPA 2.2.3 and 2.2.4 are excluded because they ship the patched version (3.0.7-28.el9_4).

### Proposed Jira Update

```
jira.edit_issue(TC-8005, fields={
  "versions": [
    {"name": "RHTPA 2.2.0"},
    {"name": "RHTPA 2.2.1"},
    {"name": "RHTPA 2.2.2"}
  ]
})
```

Version IDs are resolved dynamically via `getJiraIssueTypeMetaWithFields` — not hardcoded.

### Proposed Comment

```
Corrected Affects Versions: [RHTPA 2.0.0] → [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

[Comment Footnote]
```
