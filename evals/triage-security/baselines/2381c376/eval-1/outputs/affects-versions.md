# Step 3 -- Affects Versions Correction

## Step 3.1 -- Jira Version Discovery

Available Jira versions would be discovered dynamically via `getJiraIssueTypeMetaWithFields` for the Vulnerability issue type (ID: 10024) in project TC. The Jira version prefix is **RHTPA**.

Expected version registry (filtered by RHTPA prefix):

| Jira ID | Name | Released | Release Date |
|---------|------|----------|--------------|
| (dynamic) | RHTPA 2.1.0 | yes | 2025-09-15 |
| (dynamic) | RHTPA 2.1.1 | yes | 2025-11-20 |
| (dynamic) | RHTPA 2.2.0 | yes | 2025-12-03 |
| (dynamic) | RHTPA 2.2.1 | yes | 2026-02-05 |
| (dynamic) | RHTPA 2.2.2 | yes | 2026-02-23 |
| (dynamic) | RHTPA 2.2.3 | yes | 2026-03-23 |
| (dynamic) | RHTPA 2.2.4 | yes | 2026-05-04 |

Note: Jira version IDs would be discovered at runtime -- no hardcoded IDs.

## Step 3.2 -- Compare and Correct

### Current Affects Versions

PSIRT assigned: **RHTPA 2.0.0**

### Stream Scope

This issue is scoped to stream **2.2.x** (per the `[rhtpa-2.2]` suffix in the summary). Only versions belonging to the 2.2.x stream are included in the Affects Versions correction. The 2.1.x stream's affected versions (2.1.0, 2.1.1) are tracked by companion/sibling CVE Jiras for that stream.

### Version Impact (2.2.x stream only)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| RHTPA 2.2.0 | 0.11.9 | YES |
| RHTPA 2.2.1 | 0.11.12 | YES |
| RHTPA 2.2.2 | 0.11.12 (retag of 2.2.1) | YES |
| RHTPA 2.2.3 | 0.11.14 | NO |
| RHTPA 2.2.4 | 0.11.14 | NO |

### Correction

**PSIRT version is wrong.** RHTPA 2.0.0 does not correspond to any configured version stream -- no 2.0.x stream exists in the Version Streams table. The PSIRT assignment is incorrect.

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

### Proposed Jira Mutation (not executed)

After engineer confirmation, the following update would be applied:

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<rhtpa-2.2.0-jira-id>"},
    {"id": "<rhtpa-2.2.1-jira-id>"},
    {"id": "<rhtpa-2.2.2-jira-id>"}
  ]
})
```

Jira version IDs would be resolved from the `getJiraIssueTypeMetaWithFields` response in Step 3.1.

### Proposed Comment (not executed)

A comment would be posted to TC-8001 documenting the correction:

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

RHTPA 2.0.0 does not match any configured version stream. Lock file evidence shows:
- RHTPA 2.2.0 (v0.4.5): quinn-proto 0.11.9 -- AFFECTED (< 0.11.14)
- RHTPA 2.2.1 (v0.4.8): quinn-proto 0.11.12 -- AFFECTED (< 0.11.14)
- RHTPA 2.2.2 (v0.4.9): retag of 2.2.1 -- AFFECTED
- RHTPA 2.2.3 (v0.4.11): quinn-proto 0.11.14 -- NOT AFFECTED (>= fix threshold)
- RHTPA 2.2.4 (v0.4.12): quinn-proto 0.11.14 -- NOT AFFECTED (>= fix threshold)
```

Note: If a ProdSec Jira account ID were configured, an @mention would be appended before the Comment Footnote. No ProdSec account ID is configured in the mock Security Configuration, so the @mention is omitted.
