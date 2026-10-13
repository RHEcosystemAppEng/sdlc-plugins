# Step 3 -- Affects Versions Correction: TC-8005

## Stream Scope

This issue is scoped to stream **2.2.x** (from summary suffix `[rhtpa-2.2]`). Only versions belonging to the 2.2.x stream are included in the Affects Versions correction. The 2.1.x versions belong to a companion/sibling issue.

## Version Impact (scoped to 2.2.x)

| Version | openssl-libs | Affected? |
|---------|-------------|-----------|
| 2.2.0 | 3.0.7-25.el9_3 | YES |
| 2.2.1 | 3.0.7-27.el9_4 | YES |
| 2.2.2 | 3.0.7-27.el9_4 (retag of 2.2.1) | YES |
| 2.2.3 | 3.0.7-28.el9_4 | NO |
| 2.2.4 | 3.0.7-28.el9_4 | NO |

## Affects Versions Correction

**PSIRT version is wrong.** RHTPA 2.0.0 does not exist in the configured version streams -- there is no 2.0.x stream.

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

**Rationale**: Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md:
- RHTPA 2.2.0 (tag v0.4.5): openssl-libs 3.0.7-25.el9_3 -- within affected range (< 3.0.7-28.el9_4)
- RHTPA 2.2.1 (tag v0.4.8): openssl-libs 3.0.7-27.el9_4 -- within affected range (< 3.0.7-28.el9_4)
- RHTPA 2.2.2 (tag v0.4.9): retag of 2.2.1 -- same version, within affected range
- RHTPA 2.2.3 (tag v0.4.11): openssl-libs 3.0.7-28.el9_4 -- at fix version, NOT affected
- RHTPA 2.2.4 (tag v0.4.12): openssl-libs 3.0.7-28.el9_4 -- at fix version, NOT affected

Scoped to stream 2.2.x per issue suffix `[rhtpa-2.2]`.

## Jira Update

The Affects Versions field would be updated using dynamically discovered Jira version IDs (from `getJiraIssueTypeMetaWithFields`). The Jira version IDs are not hardcoded -- they are resolved at runtime by matching the version names against the `allowedValues` for the `versions` field filtered by the `RHTPA` prefix.

A comment would be posted documenting the correction:

> Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
> Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md.
> Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].
> RHTPA 2.0.0 does not correspond to any configured version stream.
