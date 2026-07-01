# Step 3 -- Affects Versions Correction

## Step 3.1 -- Jira Version Discovery

Proposed: dynamically discover available Jira versions by calling `getJiraIssueTypeMetaWithFields` for Vulnerability issue type (10024) in project TC, filtered by the Jira version prefix `RHTPA`.

The following versions would be discovered (referenced by name from the supportability matrix, not hardcoded Jira version IDs -- Important Rule 6):

| Name | Released | Stream |
|------|----------|--------|
| RHTPA 2.1.0 | yes | 2.1.x |
| RHTPA 2.1.1 | yes | 2.1.x |
| RHTPA 2.2.0 | yes | 2.2.x |
| RHTPA 2.2.1 | yes | 2.2.x |
| RHTPA 2.2.2 | yes | 2.2.x |
| RHTPA 2.2.3 | yes | 2.2.x |
| RHTPA 2.2.4 | yes | 2.2.x |

## Step 3.2 -- Compare and Correct Affects Versions

### Scope

This issue is **unscoped** (no stream suffix) -- it covers all streams. Therefore, the Affects Versions correction includes all actually affected versions across all streams (not scoped to a single stream).

### Version Impact Evidence

From the version impact table:
- **RHTPA 2.1.0**: h2 0.4.5 -- **AFFECTED** (< 0.4.8)
- **RHTPA 2.1.1**: h2 0.4.5 -- **AFFECTED** (< 0.4.8)
- **RHTPA 2.2.0**: h2 0.4.8 -- NOT affected (>= 0.4.8)
- **RHTPA 2.2.1**: h2 0.4.8 -- NOT affected (>= 0.4.8)
- **RHTPA 2.2.2**: retag of 2.2.1 -- NOT affected
- **RHTPA 2.2.3**: h2 0.4.9 -- NOT affected (>= 0.4.8)
- **RHTPA 2.2.4**: h2 0.4.9 -- NOT affected (>= 0.4.8)

### Proposed Correction

```
Current Affects Versions:  [RHTPA 2.1.0, RHTPA 2.2.0]
Proposed Affects Versions: [RHTPA 2.1.0, RHTPA 2.1.1]
```

**Changes:**
- **RHTPA 2.1.0** -- retained (confirmed affected: h2 0.4.5 < 0.4.8)
- **RHTPA 2.1.1** -- added (confirmed affected: h2 0.4.5 < 0.4.8, missing from PSIRT assignment)
- **RHTPA 2.2.0** -- removed (not affected: h2 0.4.8 >= 0.4.8, PSIRT incorrectly included this version)

The correction includes only the actually affected versions (2.1.x versions). The 2.2.x versions are excluded because all 2.2.x releases ship h2 >= 0.4.8, which is at or above the fix threshold.

### Proposed Jira Mutation

After engineer confirmation, the following mutation would be executed:

```
jira.edit_issue("TC-8004", fields={
  "versions": [{"id": "<RHTPA-2.1.0-id>"}, {"id": "<RHTPA-2.1.1-id>"}]
})
```

(Version IDs resolved dynamically from Step 3.1 discovery -- Important Rule 6)

### Proposed Jira Comment

```
Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].

Based on lock file analysis at pinned commits from security-matrix.md:
- RHTPA 2.1.0 (v0.3.8): h2 0.4.5 -- affected (< 0.4.8)
- RHTPA 2.1.1 (v0.3.12): h2 0.4.5 -- affected (< 0.4.8)
- RHTPA 2.2.0 (v0.4.5): h2 0.4.8 -- not affected (>= 0.4.8)

RHTPA 2.2.0 removed: ships h2 0.4.8 (at fix threshold).
RHTPA 2.1.1 added: ships h2 0.4.5 (below fix threshold).

This issue is unscoped (no stream suffix) -- correction covers all streams.

---
_Comment posted by `sdlc-workflow:triage-security`_
```

**Note**: No ProdSec Jira account ID is configured in this project's Security Configuration, so the ProdSec @mention is omitted silently.
