# Step 3 -- Affects Versions Correction: TC-8004

## Current vs Proposed Affects Versions

The issue is **unscoped** (no stream suffix), so the Affects Versions correction includes all actually affected versions across all streams.

### PSIRT-assigned Affects Versions (current)

- RHTPA 2.1.0
- RHTPA 2.2.0

### Version Impact Evidence

| Version | h2 version | Affected? |
|---------|------------|-----------|
| RHTPA 2.1.0 | 0.4.5 | YES |
| RHTPA 2.1.1 | 0.4.5 | YES |
| RHTPA 2.2.0 | 0.4.8 | NO |
| RHTPA 2.2.1 | 0.4.8 | NO |
| RHTPA 2.2.2 | 0.4.8 | NO (retag of 2.2.1) |
| RHTPA 2.2.3 | 0.4.9 | NO |
| RHTPA 2.2.4 | 0.4.9 | NO |

### Proposed Correction

```
Current:  [RHTPA 2.1.0, RHTPA 2.2.0]
Proposed: [RHTPA 2.1.0, RHTPA 2.1.1]
```

**Changes:**
- **Added**: RHTPA 2.1.1 -- lock file analysis confirms h2 0.4.5 (vulnerable) at pinned commit v0.3.12
- **Removed**: RHTPA 2.2.0 -- lock file analysis confirms h2 0.4.8 (fixed) at pinned commit v0.4.5; this version is NOT affected

### Rationale

PSIRT assigned Affects Versions based on scan-time heuristics. Lock file analysis at the actual pinned source commits from the supportability matrix shows:

1. **RHTPA 2.1.0** (v0.3.8): ships h2 0.4.5 -- **affected** (below fix threshold 0.4.8). Correctly included by PSIRT.
2. **RHTPA 2.1.1** (v0.3.12): ships h2 0.4.5 -- **affected** (below fix threshold 0.4.8). Missing from PSIRT assignment.
3. **RHTPA 2.2.0** (v0.4.5): ships h2 0.4.8 -- **not affected** (at fix threshold). Incorrectly included by PSIRT.

The corrected Affects Versions include only versions that actually ship the vulnerable h2 dependency (versions before 0.4.8).

### Jira Update

After engineer confirmation, the Affects Versions field would be updated:

```
jira.edit_issue("TC-8004", fields={
  "versions": [
    {"id": "<jira-id-for-RHTPA-2.1.0>"},
    {"id": "<jira-id-for-RHTPA-2.1.1>"}
  ]
})
```

Version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (not hardcoded).

### Comment

A comment documenting the correction would be posted to TC-8004:

> Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].
>
> Based on lock file analysis at pinned commits from security-matrix.md:
> - RHTPA 2.1.0 (v0.3.8): h2 = 0.4.5 (affected)
> - RHTPA 2.1.1 (v0.3.12): h2 = 0.4.5 (affected)
> - RHTPA 2.2.0 (v0.4.5): h2 = 0.4.8 (not affected -- at fix threshold)
>
> Removed RHTPA 2.2.0 (ships fixed h2 version). Added RHTPA 2.1.1 (ships vulnerable h2 version).
> This issue is unscoped -- correction includes all affected versions across all streams.

## Sibling/Duplicate Check (Step 4)

JQL search for sibling Vulnerability issues with the same CVE label returned **no results** (assumed per eval instructions). No duplicates or companion issues exist.

Since no siblings were found and the issue is unscoped, no cross-stream coordination is needed.
