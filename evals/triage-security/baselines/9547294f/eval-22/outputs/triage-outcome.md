# Triage Outcome for TC-8021

## Summary

TC-8021 tracks CVE-2026-31812 (quinn-proto < 0.11.14) scoped to the **2.2.x** stream.

## Step 0 -- Configuration Validation

Configuration successfully validated:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Jira version prefix: RHTPA
- Vulnerability issue type ID: 10024
- Upstream Affected Component custom field: customfield_10632 (configured)

## Step 0.3 -- Matrix Staleness Check

The security-matrix.md `Last-Updated` timestamp is `2026-06-28T10:00:00Z` (3 days ago as of 2026-07-01). This is within the 14-day threshold. Proceeding without staleness warning.

## Step 1 -- Data Extraction

CVE-2026-31812 identified in quinn-proto, affected versions < 0.11.14, fixed in 0.11.14. Ecosystem: Cargo. Stream scope: 2.2.x (from suffix `[rhtpa-2.2]`).

## Step 1.5 -- External CVE Data Enrichment

External API queries skipped per eval constraints (no WebFetch calls permitted). Using Jira description data: fix threshold 0.11.14.

## Step 2 -- Version Impact Analysis

Version impact table for CVE-2026-31812 (quinn-proto < 0.11.14), scoped to 2.2.x stream:

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.11.14 | NO | |
| 2.2.4 | 0.11.14 | NO | |

Versions 2.2.0 through 2.2.2 ship quinn-proto versions below 0.11.14 and are affected.
Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14, which is the fixed version, and are not affected.

## Step 3 -- Affects Versions Correction

Current Affects Versions: [RHTPA 2.0.0]
Proposed Affects Versions: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]

The PSIRT-assigned version RHTPA 2.0.0 does not match any version in the 2.2.x stream supportability matrix. Based on lock file analysis, the affected versions within the 2.2.x stream scope are 2.2.0, 2.2.1, and 2.2.2.

Proposed correction: `Current: [RHTPA 2.0.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

## Step 4 -- Duplicate, Sibling, and Overlap Check

Sibling and duplicate checks would be performed via JQL. Overlap check using customfield_10632 (quinn-proto) for cross-CVE detection.

## Step 5 -- Version Lifecycle Check

Version lifecycle verification would be performed against the Product pages URL.

## Step 6 -- Already Fixed Check

Already-fixed check against resolved sibling issues.

## Step 7 -- Concurrent Triage Detection

**Concurrent triage check executed for upstream component quinn-proto.**

JQL query:
```
project = TC AND issuetype = 10024 AND cf[10632] ~ 'quinn-proto' AND status IN ('In Progress', 'Code Review') AND key != TC-8021
```

**Result: Zero results returned.** No concurrent triages detected on the same upstream component.

The analysis proceeds directly to Case A/B/C branching without presenting any concurrent triage warning or wait/skip/proceed options to the engineer.

## Step 8 -- Remediation (Case A)

Since versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream are affected, this is **Case A: Affected -- create remediation tasks**.

The ecosystem is **Cargo** (source dependency), so two tasks would be created:

### Task 1: Upstream Backport

**Proposed action**: Create a Jira Task for the upstream backport.

- Summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)"
- Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`
- Link: Depend on TC-8021

### Task 2: Downstream Propagation

**Proposed action**: Create a Jira Task for downstream propagation.

- Summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)"
- Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`
- Link: Depend on TC-8021, Blocked by upstream task

### Cross-Stream Check

The 2.1.x stream also shows affected versions (2.1.0 and 2.1.1 ship quinn-proto 0.11.9), but since TC-8021 is scoped to the 2.2.x stream, cross-stream impact would be noted via a comment (Step 8 Case B) if applicable, but remediation tasks are only created for the 2.2.x stream within the issue's scope.

### Post-Triage

- Add `ai-cve-triaged` label to TC-8021
- Post summary comment with version impact table, Affects Versions correction, remediation task links, and @mention of the issue reporter
