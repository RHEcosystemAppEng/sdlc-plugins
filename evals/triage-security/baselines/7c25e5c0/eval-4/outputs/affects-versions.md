# Step 3 — Affects Versions Correction

## 3.1 — Available Jira Versions

Proposed query: `getJiraIssueTypeMetaWithFields(projectIdOrKey: "TC", issueTypeId: "10024")` to discover versions matching prefix "RHTPA".

## 3.2 — Compare and Correct

Since this issue is **unscoped** (no stream suffix), Affects Versions should include all actually affected versions across all streams.

**Current Affects Versions (PSIRT-assigned):** RHTPA 2.1.0, RHTPA 2.2.0

**Lock-file-verified impact:**
- RHTPA 2.1.0: h2 0.4.5 → **YES** (affected)
- RHTPA 2.1.1: h2 0.4.5 → **YES** (affected, missing from PSIRT assignment)
- RHTPA 2.2.0: h2 0.4.8 → **NO** (not affected, incorrectly included by PSIRT)
- RHTPA 2.2.1: h2 0.4.8 → **NO** (not affected)
- RHTPA 2.2.2: retag of 2.2.1 → **NO** (not affected)
- RHTPA 2.2.3: h2 0.4.9 → **NO** (not affected)
- RHTPA 2.2.4: h2 0.4.9 → **NO** (not affected)

**Proposed correction:**

```
Current:  [RHTPA 2.1.0, RHTPA 2.2.0]
Proposed: [RHTPA 2.1.0, RHTPA 2.1.1]
```

**Changes:**
- **Added**: RHTPA 2.1.1 — lock file confirms h2 0.4.5 (affected)
- **Removed**: RHTPA 2.2.0 — lock file confirms h2 0.4.8 (at fix threshold, not affected)

**Proposed Jira mutation (pending engineer confirmation):**

```
jira.edit_issue("TC-8004", fields={
  "versions": [
    {"name": "RHTPA 2.1.0"},
    {"name": "RHTPA 2.1.1"}
  ]
})
```

Version names are from the Jira version registry (dynamic discovery via `getJiraIssueTypeMetaWithFields`), not hardcoded IDs.

**Proposed comment (pending confirmation):**

> Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] → [RHTPA 2.1.0, RHTPA 2.1.1].
> Based on lock file analysis at pinned commits from security-matrix.md.
> RHTPA 2.2.0 removed — ships h2 0.4.8 (at or above fix threshold).
> RHTPA 2.1.1 added — ships h2 0.4.5 (below fix threshold 0.4.8).
> This issue is unscoped — correction covers all affected versions across all streams.
