# Ready for QA — Filtering Analysis

## Overview

Query 3 searched for triaged CVEs that are not yet Closed, Verified, or ON_QA, to identify issues whose remediation work is complete and are candidates for ON_QA transition.

**JQL**: `project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC`

**Results returned**: 3 issues

## Filtering Criteria

For each result, the `issuelinks` field is inspected for linked Tasks with link type "Depend":

1. **ALL linked remediation Tasks are Done or Closed** --> include in Ready for QA list
2. **ANY linked Task is still open** --> exclude (remediation still in progress)
3. **NO linked Tasks with type "Depend" exist** --> exclude (no remediation to verify)

## Per-Issue Analysis

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status**: Modified
- **Created**: 2026-05-15
- **Linked remediation Tasks (Depend)**:
  - TC-9021: Task, status **Done**
  - TC-9022: Task, status **Closed**
- **Assessment**: ALL linked remediation Tasks are in a completed state (Done or Closed).
- **Result**: **QUALIFIED — Ready for QA**
- **Recommendation**: Consider transitioning TC-9020 to ON_QA.

---

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status**: In Progress
- **Created**: 2026-05-10
- **Linked remediation Tasks (Depend)**:
  - TC-9024: Task, status **Done**
  - TC-9025: Task, status **In Progress**
- **Assessment**: TC-9025 is still In Progress. Not all linked remediation Tasks are complete.
- **Result**: **EXCLUDED — remediation in progress**
- **Reason**: At least one linked Task (TC-9025) has an open status (In Progress). Remediation work is not yet finished.

---

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status**: Modified
- **Created**: 2026-05-05
- **Linked remediation Tasks (Depend)**: None
- **Assessment**: No issue links with type "Depend" found. There are no remediation Tasks to verify completion against.
- **Result**: **EXCLUDED — no remediation to verify**
- **Reason**: Without linked remediation Tasks (Depend link type), there is no evidence of completed remediation work. This issue may need remediation tasks created, or its remediation may be tracked outside of Jira issue links.

## Summary

| Issue | CVE | Status | Depend Links | All Tasks Done? | Ready for QA? |
|-------|-----|--------|--------------|-----------------|---------------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | No |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A | No |

**1 of 3 candidates qualified for Ready for QA**: TC-9020.
