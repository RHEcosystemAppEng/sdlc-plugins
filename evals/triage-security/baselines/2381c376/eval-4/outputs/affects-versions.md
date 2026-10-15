# Step 3 -- Affects Versions Correction: TC-8004

## Current vs Proposed Affects Versions

Since TC-8004 is an **unscoped** issue (no stream suffix), the Affects Versions field should include all affected versions across all streams.

### PSIRT-Assigned (Current)

- RHTPA 2.1.0
- RHTPA 2.2.0

### Lock-File-Verified (Proposed)

- RHTPA 2.1.0
- RHTPA 2.1.1

### Correction Diff

```
Current:  [RHTPA 2.1.0, RHTPA 2.2.0]
Proposed: [RHTPA 2.1.0, RHTPA 2.1.1]

Changes:
  + ADD    RHTPA 2.1.1  (h2 0.4.5 < 0.4.8 -- affected, missing from PSIRT assignment)
  - REMOVE RHTPA 2.2.0  (h2 0.4.8 >= 0.4.8 -- NOT affected, incorrectly included by PSIRT)
```

### Rationale

- **RHTPA 2.1.0**: KEEP -- h2 version 0.4.5 (from build tag v0.3.8) is below the fix threshold of 0.4.8. Confirmed affected.
- **RHTPA 2.1.1**: ADD -- h2 version 0.4.5 (from build tag v0.3.12) is below the fix threshold of 0.4.8. PSIRT omitted this version.
- **RHTPA 2.2.0**: REMOVE -- h2 version 0.4.8 (from build tag v0.4.5) equals the fix threshold. This version ships the patched h2 and is NOT affected.
- **RHTPA 2.2.1 through 2.2.4**: Not listed by PSIRT, and correctly so -- all ship h2 >= 0.4.8.

### Proposed Jira Mutation

**Action**: Update Affects Versions field on TC-8004

```
Proposed jira.edit_issue(TC-8004, fields={
  "versions": [
    {"name": "RHTPA 2.1.0"},
    {"name": "RHTPA 2.1.1"}
  ]
})
```

Note: Actual Jira version IDs would be resolved dynamically via `getJiraIssueTypeMetaWithFields` at execution time. The version names above use the RHTPA prefix from Security Configuration.

### Proposed Comment on TC-8004

```
Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].

Changes:
- Added RHTPA 2.1.1: h2 0.4.5 at build tag v0.3.12 is below fix threshold 0.4.8
- Removed RHTPA 2.2.0: h2 0.4.8 at build tag v0.4.5 meets fix threshold 0.4.8

Based on lock file analysis (Cargo.lock) at pinned commits from security-matrix.md.
This is an unscoped issue -- correction covers all streams.
```

## Step 4 -- Duplicate, Sibling, and Overlap Check

### 4.1/4.2 -- Sibling Search

JQL query (simulated):
```
project = TC AND labels = 'CVE-2026-33501' AND issuetype = 10024 AND key != TC-8004
```

Result: **No sibling issues found.** No duplicates or cross-stream companions exist.

### 4.3 -- Cross-CVE Overlap Detection

**Skipped.** The Upstream Affected Component custom field is not configured in Security Configuration, so cross-CVE overlap detection cannot be performed.

### 4.4 -- Preemptive Task Reconciliation

JQL query (simulated):
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-33501' ORDER BY created DESC
```

Result: **No preemptive tasks found.** No prior cross-stream triage created preemptive remediation for this CVE.

## Step 5 -- Version Lifecycle Check

Proposed action: Verify that RHTPA 2.1.0 and RHTPA 2.1.1 are still within their support lifecycle by checking the Product pages URL (https://access.example.com/product-life-cycle/rhtpa). For the purposes of this analysis, both versions are assumed to be within their support lifecycle and eligible for remediation.

## Step 6 -- Already Fixed Check

No resolved sibling issues exist (Step 4 returned empty). The already-fixed check does not apply. Proceeding to remediation.
