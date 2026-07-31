# Affects Versions Correction — TC-8004

## Step 3: Affects Versions Correction

### Step 3.1 — Jira Version Registry (mock)

Jira Versions matching "RHTPA":

| Jira ID | Name | Released | Release Date |
|---------|------|----------|--------------|
| 60001 | RHTPA 2.1.0 | yes | 2025-09-15 |
| 60002 | RHTPA 2.1.1 | yes | 2025-11-20 |
| 60003 | RHTPA 2.2.0 | yes | 2025-12-03 |
| 60004 | RHTPA 2.2.1 | yes | 2026-02-05 |
| 60005 | RHTPA 2.2.2 | yes | 2026-02-23 |
| 60006 | RHTPA 2.2.3 | yes | 2026-03-23 |
| 60007 | RHTPA 2.2.4 | yes | 2026-05-04 |

### Step 3.2 — Compare and Correct

**Scope**: This issue is **unscoped** (no stream suffix), so the correction includes all affected versions across all streams. Per Step 3.2: "If the issue is unscoped, include all affected versions across all streams."

**Version impact table results (from Step 2):**
- RHTPA 2.1.0: **YES** (affected — h2 0.4.5)
- RHTPA 2.1.1: **YES** (affected — h2 0.4.5)
- RHTPA 2.2.0: **NO** (not affected — h2 0.4.8)
- RHTPA 2.2.1: **NO** (not affected — h2 0.4.8)
- RHTPA 2.2.2: **NO** (not affected — retag of 2.2.1)
- RHTPA 2.2.3: **NO** (not affected — h2 0.4.9)
- RHTPA 2.2.4: **NO** (not affected — h2 0.4.9)

**Correction:**

The PSIRT-assigned Affects Versions are **incorrect and incomplete**:
- RHTPA 2.2.0 is listed but is NOT affected (ships h2 0.4.8, which is at the fix threshold)
- RHTPA 2.1.1 is NOT listed but IS affected (ships h2 0.4.5)

```
Current Affects Versions:  [RHTPA 2.1.0, RHTPA 2.2.0]
Proposed Affects Versions: [RHTPA 2.1.0, RHTPA 2.1.1]
```

Changes:
- **Remove** RHTPA 2.2.0 — version 2.2.0 ships h2 0.4.8 (at fix threshold, not affected)
- **Add** RHTPA 2.1.1 — version 2.1.1 ships h2 0.4.5 (within affected range)

Only the actually affected versions (2.1.x stream) are included. The 2.2.x versions are excluded because all 2.2.x versions ship h2 >= 0.4.8, which is at or above the fix threshold.

### Proposed Jira Update

```
jira.edit_issue("TC-8004", fields={
  "versions": [{"id": "60001"}, {"id": "60002"}]
})
```

### Comment

```
Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].
Based on lock file analysis at pinned commits from security-matrix.md.
Issue is unscoped — correction includes all affected versions across all streams.
RHTPA 2.2.0 removed (ships h2 0.4.8, not affected). RHTPA 2.1.1 added (ships h2 0.4.5, affected).
```
