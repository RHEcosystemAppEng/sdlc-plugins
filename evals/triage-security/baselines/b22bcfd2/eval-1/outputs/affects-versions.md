# Step 3 -- Affects Versions Correction

## Step 3.1 -- Discover Available Jira Versions

Proposed call to discover available versions:

```
jira.getJiraIssueTypeMetaWithFields(
  projectIdOrKey: "TC",
  issueTypeId: "10024"
)
```

Filtered by Jira version prefix `RHTPA`, the available versions include (dynamically discovered, not hardcoded):

| Name | Released | Notes |
|------|----------|-------|
| RHTPA 2.1.0 | yes | Stream 2.1.x |
| RHTPA 2.1.1 | yes | Stream 2.1.x |
| RHTPA 2.2.0 | yes | Stream 2.2.x |
| RHTPA 2.2.1 | yes | Stream 2.2.x |
| RHTPA 2.2.2 | yes | Stream 2.2.x |
| RHTPA 2.2.3 | yes | Stream 2.2.x |
| RHTPA 2.2.4 | yes | Stream 2.2.x |

Version names are referenced from the supportability matrix. Jira version IDs would be discovered dynamically at runtime via `getJiraIssueTypeMetaWithFields` (Important Rule 6: use dynamic version discovery, never hardcode Jira version IDs).

## Step 3.2 -- Compare and Correct Affects Versions

### Current vs Proposed

The issue is **scoped to stream 2.2.x** (suffix `[rhtpa-2.2]`). Only 2.2.x versions are included in the Affects Versions correction; 2.1.x versions belong to a sibling issue (Step 4).

From the version impact table, the affected 2.2.x versions are: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2.

```
Current Affects Versions:  [RHTPA 2.0.0]
Proposed Affects Versions: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

**PSIRT-assigned version is wrong**: `RHTPA 2.0.0` does not correspond to any version in the supportability matrix or configured Version Streams. The lock file analysis confirms that versions 2.2.0, 2.2.1, and 2.2.2 (all shipping quinn-proto < 0.11.14) are affected within the 2.2.x stream scope.

Versions 2.2.3 and 2.2.4 are excluded because they ship quinn-proto 0.11.14, which is outside the affected range (< 0.11.14).

### Proposed Jira Mutation (requires engineer confirmation)

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<dynamically-discovered-id-for-RHTPA-2.2.0>"},
    {"id": "<dynamically-discovered-id-for-RHTPA-2.2.1>"},
    {"id": "<dynamically-discovered-id-for-RHTPA-2.2.2>"}
  ]
})
```

### Proposed Comment (requires engineer confirmation)

```
jira.add_comment("TC-8001",
  "Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
  Based on lock file analysis at pinned commits from security-matrix.md.
  Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

  Evidence:
  - RHTPA 2.2.0 (tag v0.4.5): quinn-proto 0.11.9 < 0.11.14 -> affected
  - RHTPA 2.2.1 (tag v0.4.8): quinn-proto 0.11.12 < 0.11.14 -> affected
  - RHTPA 2.2.2 (tag v0.4.8): retag of 2.2.1 -> affected (same as 2.2.1)
  - RHTPA 2.2.3 (tag v0.4.11): quinn-proto 0.11.14 >= 0.11.14 -> not affected
  - RHTPA 2.2.4 (tag v0.4.12): quinn-proto 0.11.14 >= 0.11.14 -> not affected

  ---
  _Posted by sdlc-workflow skill: triage-security_")
```

All version names above are referenced from the supportability matrix and would be matched to Jira version IDs via dynamic discovery (Important Rule 6).
