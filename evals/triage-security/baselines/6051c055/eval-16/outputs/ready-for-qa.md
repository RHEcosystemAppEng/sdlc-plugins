# Ready for QA — Filtering Analysis

## Overview

Query 3 searches for triaged CVE Vulnerability issues that are not yet closed, verified, or in QA:

**JQL**: `project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC`

3 candidate issues were returned. Each was evaluated by inspecting its `issuelinks` for linked Tasks with the "Depend" link type. For each linked Task, the status was checked to determine whether all remediation work is complete.

## Filtering Criteria

An issue qualifies as "Ready for QA" only when **all** of the following are true:
1. The issue has at least one linked Task with link type "Depend"
2. Every such linked Task has a terminal status (Done or Closed)

An issue is **excluded** if:
- Any linked remediation Task is still open (not Done/Closed) -- remediation is in progress
- No linked Tasks with link type "Depend" exist -- no remediation to verify

## Candidate Analysis

### TC-9020 -- INCLUDED (Ready for QA)

- **Summary**: CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]
- **Status**: Modified
- **Created**: 2026-05-15
- **Linked remediation Tasks (Depend)**:
  - TC-9021: **Done** (complete)
  - TC-9022: **Closed** (complete)
- **Assessment**: All 2 linked remediation Tasks have terminal statuses. Remediation is fully complete.
- **Recommendation**: Consider transitioning TC-9020 to ON_QA. All remediation work has been completed and is ready for quality assurance verification.

### TC-9023 -- EXCLUDED (remediation in progress)

- **Summary**: CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]
- **Status**: In Progress
- **Created**: 2026-05-10
- **Linked remediation Tasks (Depend)**:
  - TC-9024: **Done** (complete)
  - TC-9025: **In Progress** (still open)
- **Assessment**: 1 of 2 linked remediation Tasks is still in progress. TC-9025 has not reached a terminal status.
- **Reason for exclusion**: Remediation is not yet complete. TC-9025 must reach Done or Closed before this issue can move to QA.

### TC-9026 -- EXCLUDED (no remediation to verify)

- **Summary**: CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]
- **Status**: Modified
- **Created**: 2026-05-05
- **Linked remediation Tasks (Depend)**: None
- **Assessment**: No linked Tasks with "Depend" link type were found on this issue.
- **Reason for exclusion**: Without linked remediation Tasks, there is no completed remediation to verify in QA. This issue may need remediation tasks created, or it may have been triaged with a different outcome (e.g., closed as not affected and later reopened).

## Summary

| Issue | Status | Linked Tasks | All Complete? | Result |
|-------|--------|--------------|---------------|--------|
| TC-9020 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | **Ready for QA** |
| TC-9023 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | Excluded -- remediation in progress |
| TC-9026 | Modified | (none) | N/A | Excluded -- no remediation to verify |

**1 of 3 candidates qualified for ON_QA transition.**
