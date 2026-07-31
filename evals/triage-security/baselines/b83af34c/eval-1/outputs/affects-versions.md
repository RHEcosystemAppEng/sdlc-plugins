# Step 3 -- Affects Versions Correction

## Proposed Affects Versions Change for TC-8001

The PSIRT-assigned Affects Versions are incorrect. The correction is scoped to the 2.2.x stream (per the issue's `[rhtpa-2.2]` suffix). Versions from the 2.1.x stream are excluded from this issue's Affects Versions -- they belong to a companion issue for that stream.

### Diff

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

### Rationale

- **RHTPA 2.0.0** is not a valid version in the supportability matrix. There is no 2.0.x stream configured. PSIRT assigned this version incorrectly -- it does not correspond to any shipped product version.
- **RHTPA 2.2.0** -- ships quinn-proto 0.11.9 (at pinned tag `v0.4.5`), which is within the affected range (< 0.11.14). AFFECTED.
- **RHTPA 2.2.1** -- ships quinn-proto 0.11.12 (at pinned tag `v0.4.8`), which is within the affected range (< 0.11.14). AFFECTED.
- **RHTPA 2.2.2** -- retag of 2.2.1 (same backend source at `v0.4.8`). Carries forward affected status. AFFECTED.
- **RHTPA 2.2.3** -- ships quinn-proto 0.11.14 (at pinned tag `v0.4.11`), which is the fixed version. NOT AFFECTED -- excluded.
- **RHTPA 2.2.4** -- ships quinn-proto 0.11.14 (at pinned tag `v0.4.12`), which is the fixed version. NOT AFFECTED -- excluded.

### Version Names

Version names are referenced from the supportability matrix using the Jira version prefix RHTPA (e.g., RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2). Actual Jira version IDs would be discovered dynamically at runtime via `getJiraIssueTypeMetaWithFields` (Important Rule 6) -- no hardcoded version IDs are used.

### Proposed Comment

After engineer confirmation, the following comment would be proposed for TC-8001:

> Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
> Based on lock file analysis at pinned commits from security-matrix.md.
> Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

This is a **proposed action** pending engineer confirmation. No Jira mutation has been executed.
