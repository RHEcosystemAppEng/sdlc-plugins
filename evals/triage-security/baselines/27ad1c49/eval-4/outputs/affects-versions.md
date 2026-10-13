# Affects Versions Correction — TC-8004 (CVE-2026-33501)

## Step 3: Affects Versions Correction

### 3.1 — Jira Version Discovery

_(Simulated — using known RHTPA version prefix from Security Configuration)_

Jira versions matching "RHTPA":

| Jira ID | Name | Released | Relevant Stream |
|---------|------|----------|-----------------|
| (dynamic) | RHTPA 2.1.0 | yes | 2.1.x |
| (dynamic) | RHTPA 2.1.1 | yes | 2.1.x |
| (dynamic) | RHTPA 2.2.0 | yes | 2.2.x |
| (dynamic) | RHTPA 2.2.1 | yes | 2.2.x |
| (dynamic) | RHTPA 2.2.2 | yes | 2.2.x |
| (dynamic) | RHTPA 2.2.3 | yes | 2.2.x |
| (dynamic) | RHTPA 2.2.4 | yes | 2.2.x |

### 3.2 — Compare and Correct Affects Versions

**Scope**: This issue is **unscoped** (no stream suffix), so include all affected versions across all streams.

**Version impact evidence** (from lock file analysis at pinned commits):

| Version | h2 Version | Affected? |
|---------|------------|-----------|
| RHTPA 2.1.0 | 0.4.5 | **YES** (< 0.4.8) |
| RHTPA 2.1.1 | 0.4.5 | **YES** (< 0.4.8) |
| RHTPA 2.2.0 | 0.4.8 | NO (>= 0.4.8) |
| RHTPA 2.2.1 | 0.4.8 | NO (>= 0.4.8) |
| RHTPA 2.2.2 | (retag) | NO (same as 2.2.1) |
| RHTPA 2.2.3 | 0.4.9 | NO (>= 0.4.8) |
| RHTPA 2.2.4 | 0.4.9 | NO (>= 0.4.8) |

### Correction

```
Current Affects Versions:  [RHTPA 2.1.0, RHTPA 2.2.0]
Proposed Affects Versions: [RHTPA 2.1.0, RHTPA 2.1.1]
```

**Changes:**
- **Remove**: RHTPA 2.2.0 -- not affected; ships h2 0.4.8 which is at the fix threshold (>= 0.4.8)
- **Add**: RHTPA 2.1.1 -- affected; ships h2 0.4.5 which is within the vulnerable range (< 0.4.8)

**Rationale**: PSIRT included RHTPA 2.2.0 based on scan-time version assignment, but lock file analysis at the pinned source commit (v0.4.5) confirms that RHTPA 2.2.0 ships h2 0.4.8 -- the exact version where the fix was applied. PSIRT omitted RHTPA 2.1.1, which ships h2 0.4.5 (vulnerable). The correction is scoped to only affected versions based on actual dependency analysis.

### Proposed Jira Update

```
jira.edit_issue("TC-8004", fields={
  "versions": [
    {"id": "<RHTPA-2.1.0-jira-id>"},
    {"id": "<RHTPA-2.1.1-jira-id>"}
  ]
})
```

### Proposed Comment

```
Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].
Based on lock file analysis at pinned commits from security-matrix.md.

Evidence:
- RHTPA 2.2.0 removed: ships h2 0.4.8 (at fix threshold, not vulnerable)
- RHTPA 2.1.1 added: ships h2 0.4.5 (vulnerable, < 0.4.8)

This is an unscoped issue — Affects Versions include all affected versions across all streams.
Only stream 2.1.x is affected; all 2.2.x versions ship h2 >= 0.4.8.
```

## Step 4: Duplicate, Sibling, and Overlap Check

### 4.1–4.2 — Sibling Search

JQL query (simulated):
```
project = TC AND labels = 'CVE-2026-33501' AND issuetype = 10024 AND key != TC-8004
```

**Result**: No sibling issues found (JQL returns empty per eval instructions).

Since no siblings exist, there are no same-stream duplicates and no cross-stream companions to link.

### 4.3 — Cross-CVE Overlap Detection

**Skipped** — Upstream Affected Component custom field is not configured in Security Configuration.

### 4.4 — Preemptive Task Reconciliation

JQL query (simulated):
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-33501' ORDER BY created DESC
```

**Result**: No preemptive tasks found (no sibling issues exist that could have created preemptive tasks).

## Step 5: Version Lifecycle Check

_(Simulated — not calling Product pages URL in eval mode)_

Assuming all versions (2.1.x, 2.2.x) are within their support lifecycle per https://access.example.com/product-life-cycle/rhtpa. Proceeding with remediation for affected versions.

## Step 6: Already Fixed Check

No resolved sibling issues exist (Step 4 found no siblings). Proceeding to remediation.

## Step 7: Concurrent Triage Detection

**Skipped** — Upstream Affected Component custom field is not configured in Security Configuration.
