# Affects Versions Correction - TC-8004

## Step 3 - Affects Versions Correction

### Current vs Corrected Affects Versions

| | Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.1.0, RHTPA 2.2.0 |
| **Proposed (lock file evidence)** | RHTPA 2.1.0, RHTPA 2.1.1 |

### Correction Rationale

The issue is **unscoped** (no stream suffix), so all affected versions across all streams are included.

**Changes:**
- **Remove RHTPA 2.2.0**: Lock file analysis shows h2 0.4.8 at tag v0.4.5 (build for 2.2.0). Version 0.4.8 is the fixed version, so 2.2.0 is NOT affected.
- **Add RHTPA 2.1.1**: Lock file analysis shows h2 0.4.5 at tag v0.3.12 (build for 2.1.1). Version 0.4.5 is within the vulnerable range (< 0.4.8), so 2.1.1 IS affected. PSIRT missed this version.
- **Keep RHTPA 2.1.0**: Lock file analysis confirms h2 0.4.5 at tag v0.3.8 (build for 2.1.0). Correctly identified as affected by PSIRT.

No 2.2.x versions are affected -- all ship h2 >= 0.4.8.

### Proposed Jira Update

```
jira.edit_issue("TC-8004", fields={
  "versions": [
    {"name": "RHTPA 2.1.0"},
    {"name": "RHTPA 2.1.1"}
  ]
})
```

Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to affected versions only (unscoped issue -- all streams analyzed).

## Step 4 - Duplicate, Sibling, and Overlap Check

JQL search for sibling issues with the same CVE:
```
project = TC AND labels = 'CVE-2026-33501' AND issuetype = 10024 AND key != TC-8004
```

**Result: No sibling issues found.** No duplicates or companion trackers exist for this CVE.

Cross-CVE overlap detection: Skipped -- Upstream Affected Component, PS Component, and Stream custom fields are not configured in Security Configuration.

## Step 5 - Version Lifecycle Check

All affected versions (RHTPA 2.1.0, RHTPA 2.1.1) are assumed to be within support lifecycle. Proceed to remediation.

## Step 6 - Already Fixed Check

No resolved sibling issues exist (JQL returned empty in Step 4). No already-fixed scenario detected. Proceed to remediation.
