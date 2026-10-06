# Step 3 -- Affects Versions Correction

## Current vs Proposed

Since TC-8004 is **unscoped** (no stream suffix), the Affects Versions field should include all affected versions across all streams -- but only those versions that are actually affected based on lock file evidence.

| Source | Affects Versions |
|--------|------------------|
| PSIRT-assigned (current) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Lock file evidence (proposed) | RHTPA 2.1.0, RHTPA 2.1.1 |

### Changes Required

- **Remove**: RHTPA 2.2.0 -- lock file evidence shows h2 0.4.8 at tag v0.4.5, which is the fixed version. RHTPA 2.2.0 is NOT affected.
- **Add**: RHTPA 2.1.1 -- lock file evidence shows h2 0.4.5 at tag v0.3.12, which is within the affected range (< 0.4.8). PSIRT omitted this version.

### Correction Rationale

PSIRT assigned Affects Versions based on scan timing, not lock file analysis. The actual impact differs:

| Version | PSIRT says affected? | Lock file evidence | Correction |
|---------|---------------------|--------------------|------------|
| RHTPA 2.1.0 | Yes | h2 0.4.5 -- AFFECTED | Keep (correct) |
| RHTPA 2.1.1 | _(missing)_ | h2 0.4.5 -- AFFECTED | Add |
| RHTPA 2.2.0 | Yes | h2 0.4.8 -- NOT affected | Remove |

### Proposed Jira Mutation

```
jira.edit_issue("TC-8004", fields={
  "versions": [
    {"name": "RHTPA 2.1.0"},
    {"name": "RHTPA 2.1.1"}
  ]
})
```

Correction scoped to affected versions only. No 2.2.x versions are included because the 2.2.x stream is entirely unaffected.

### Comment

```
Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].

Based on lock file analysis at pinned commits from security-matrix.md:
- RHTPA 2.1.0 (v0.3.8): h2 0.4.5 -- affected (< 0.4.8)
- RHTPA 2.1.1 (v0.3.12): h2 0.4.5 -- affected (< 0.4.8)
- RHTPA 2.2.0 (v0.4.5): h2 0.4.8 -- NOT affected (= 0.4.8, the fixed version)

Removed RHTPA 2.2.0 (not affected). Added RHTPA 2.1.1 (affected but was missing).
This is an unscoped issue -- Affects Versions includes all affected versions across all streams.
```
