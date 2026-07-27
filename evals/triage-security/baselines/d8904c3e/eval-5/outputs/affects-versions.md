# Step 3 -- Affects Versions Correction: TC-8005

## Current vs Proposed

- **Current Affects Versions**: RHTPA 2.0.0
- **Proposed Affects Versions**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

## Rationale

The PSIRT-assigned Affects Versions value `RHTPA 2.0.0` is incorrect. Version
2.0.0 does not appear in any configured version stream's supportability matrix.

Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md,
the following 2.2.x versions ship a vulnerable openssl-libs (before 3.0.7-28.el9_4):

| Version | openssl-libs | Affected? |
|---------|-------------|-----------|
| 2.2.0 | 3.0.7-25.el9_3 | YES |
| 2.2.1 | 3.0.7-27.el9_4 | YES |
| 2.2.2 | 3.0.7-27.el9_4 (retag of 2.2.1) | YES |
| 2.2.3 | 3.0.7-28.el9_4 | NO (fixed) |
| 2.2.4 | 3.0.7-28.el9_4 | NO (fixed) |

This issue is scoped to stream 2.2.x per the summary suffix `[rhtpa-2.2]`.
Only 2.2.x versions are included in the Affects Versions correction. The 2.1.x
stream is also affected (2.1.0 and 2.1.1) but is tracked by its own companion
CVE issue (or requires separate PSIRT triage).

## Correction

```
Current: [RHTPA 2.0.0] --> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

Scoped to stream 2.2.x per issue suffix `[rhtpa-2.2]`.

## Jira Comment

```
Corrected Affects Versions: [RHTPA 2.0.0] --> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

Cross-stream impact: openssl-libs versions before 3.0.7-28.el9_4 also affects
stream 2.1.x (versions 2.1.0, 2.1.1). These are tracked by companion issues
or may require separate PSIRT triage.
```
