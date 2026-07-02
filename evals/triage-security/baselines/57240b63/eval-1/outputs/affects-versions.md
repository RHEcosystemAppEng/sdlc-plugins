# Step 3 -- Affects Versions Correction

## Current vs Proposed Affects Versions

TC-8001 is scoped to stream **2.2.x** (from summary suffix `[rhtpa-2.2]`).
Only versions belonging to stream 2.2.x are included in the correction.

The PSIRT-assigned Affects Versions value is **incorrect**:

| | Affects Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.0.0 |
| **Proposed (lock file evidence)** | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

### Rationale

- **RHTPA 2.0.0** does not correspond to any version in the configured Version
  Streams (2.1.x or 2.2.x). This is an incorrect PSIRT assignment -- there is
  no 2.0.x stream in the supportability matrix.

- **RHTPA 2.2.0** ships quinn-proto 0.11.9 (< 0.11.14) -- AFFECTED.

- **RHTPA 2.2.1** ships quinn-proto 0.11.12 (< 0.11.14) -- AFFECTED.

- **RHTPA 2.2.2** ships quinn-proto 0.11.12 (retag of 2.2.1, < 0.11.14) --
  AFFECTED.

- **RHTPA 2.2.3** ships quinn-proto 0.11.14 (>= 0.11.14) -- NOT affected
  (excluded from Affects Versions).

- **RHTPA 2.2.4** ships quinn-proto 0.11.14 (>= 0.11.14) -- NOT affected
  (excluded from Affects Versions).

Stream 2.1.x versions (2.1.0, 2.1.1) are also affected but belong to a
different stream -- they are NOT included in this issue's Affects Versions
because TC-8001 is scoped to 2.2.x. The 2.1.x impact is handled via
Case B cross-stream proactive remediation (see Step 8).

## PROPOSAL: Update Affects Versions

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<jira-id-for-RHTPA-2.2.0>"},
    {"id": "<jira-id-for-RHTPA-2.2.1>"},
    {"id": "<jira-id-for-RHTPA-2.2.2>"}
  ]
})
```

Version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields`
(Step 3.1). Not hardcoded.

## PROPOSAL: Post Correction Comment

```
jira.add_comment("TC-8001",
  "Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
  Based on lock file analysis at pinned commits from security-matrix.md.
  Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

  Evidence:
  - RHTPA 2.2.0 (v0.4.5): quinn-proto 0.11.9 (affected)
  - RHTPA 2.2.1 (v0.4.8): quinn-proto 0.11.12 (affected)
  - RHTPA 2.2.2 (v0.4.9): quinn-proto 0.11.12 (affected, retag of 2.2.1)
  - RHTPA 2.2.3 (v0.4.11): quinn-proto 0.11.14 (not affected)
  - RHTPA 2.2.4 (v0.4.12): quinn-proto 0.11.14 (not affected)

  [Comment Footnote]")
```
