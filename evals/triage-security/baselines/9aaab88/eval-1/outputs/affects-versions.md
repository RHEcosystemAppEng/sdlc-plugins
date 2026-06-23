# Step 3 -- Affects Versions Correction: TC-8001

## 3.1 -- Jira Version Discovery

Proposed action: Call `getJiraIssueTypeMetaWithFields` for project TC, issue type 10024 (Vulnerability), and extract versions matching prefix "RHTPA".

Expected available Jira versions (filtered by prefix RHTPA):

| Jira ID | Name | Released | Release Date |
|---------|------|----------|--------------|
| (dynamic) | RHTPA 2.1.0 | yes | 2025-09-15 |
| (dynamic) | RHTPA 2.1.1 | yes | 2025-11-20 |
| (dynamic) | RHTPA 2.2.0 | yes | 2025-12-03 |
| (dynamic) | RHTPA 2.2.1 | yes | 2026-02-05 |
| (dynamic) | RHTPA 2.2.2 | yes | 2026-02-23 |
| (dynamic) | RHTPA 2.2.3 | yes | 2026-03-23 |
| (dynamic) | RHTPA 2.2.4 | yes | 2026-05-04 |

Note: RHTPA 2.0.0 (the PSIRT-assigned version) is expected to NOT exist in Jira, or if it exists, it does not correspond to any actual release in the supportability matrix.

## 3.2 -- Affects Versions Comparison and Correction

### Stream scope

This issue is scoped to **2.2.x** (per summary suffix `[rhtpa-2.2]`). Per Step 3.2 scoping rules, only versions belonging to the 2.2.x stream should be included in the Affects Versions correction for this issue. The 2.1.x impact is reported as cross-stream impact (Step 7, Case B) and belongs to the 2.1.x stream's sibling Vulnerability issue.

### Affected 2.2.x versions from impact table

| Version | Affected? |
|---------|-----------|
| RHTPA 2.2.0 | YES (quinn-proto 0.11.9 < 0.11.14) |
| RHTPA 2.2.1 | YES (quinn-proto 0.11.12 < 0.11.14) |
| RHTPA 2.2.2 | YES (retag of 2.2.1; same as 2.2.1) |
| RHTPA 2.2.3 | NO (quinn-proto 0.11.14, fixed) |
| RHTPA 2.2.4 | NO (quinn-proto 0.11.14, fixed) |

### Proposed correction

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

**Rationale**: PSIRT assigned "RHTPA 2.0.0" which does not correspond to any supported release. Lock file analysis shows quinn-proto < 0.11.14 is present in versions 2.2.0, 2.2.1, and 2.2.2 within the scoped 2.2.x stream. Versions 2.2.3 and 2.2.4 already ship the fixed version (0.11.14) and should NOT be listed.

### Proposed Jira mutation (pending engineer confirmation)

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<RHTPA-2.2.0-jira-id>"},
    {"id": "<RHTPA-2.2.1-jira-id>"},
    {"id": "<RHTPA-2.2.2-jira-id>"}
  ]
})
```

### Proposed comment (pending engineer confirmation)

```
jira.add_comment("TC-8001", "Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

Version evidence:
- 2.2.0 (v0.4.5): quinn-proto 0.11.9 -- AFFECTED
- 2.2.1 (v0.4.8): quinn-proto 0.11.12 -- AFFECTED
- 2.2.2 (v0.4.9): retag of 2.2.1 -- AFFECTED (same as 2.2.1)
- 2.2.3 (v0.4.11): quinn-proto 0.11.14 -- NOT affected (fixed)
- 2.2.4 (v0.4.12): quinn-proto 0.11.14 -- NOT affected (fixed)")
```

### Cross-stream note

The 2.1.x stream is also affected (2.1.0 and 2.1.1 both ship quinn-proto 0.11.9). This is reported as cross-stream impact in Step 7, Case B -- the 2.1.x versions are NOT added to this issue's Affects Versions because TC-8001 is scoped to 2.2.x only.
