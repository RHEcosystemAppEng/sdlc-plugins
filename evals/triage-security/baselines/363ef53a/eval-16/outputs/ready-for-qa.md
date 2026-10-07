# Ready for QA — Filtering Analysis

## Overview

Query 3 searches for triaged Vulnerability issues that are not yet Closed, Verified, or ON_QA. Each candidate is then evaluated by inspecting its `issuelinks` for linked Tasks with link type "Depend". The filtering rules are:

1. **ALL linked remediation Tasks are Done or Closed** --> include in Ready for QA list
2. **ANY linked Task is still open** --> exclude (remediation in progress)
3. **NO linked Tasks with type "Depend" exist** --> exclude (no remediation to verify)

## Candidates Evaluated

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status**: Modified
- **Created**: 2026-05-15
- **Linked remediation Tasks (Depend)**:
  - TC-9021: Task, status **Done**
  - TC-9022: Task, status **Closed**
- **Analysis**: Both linked remediation Tasks have terminal statuses (Done and Closed). All remediation work is complete.
- **Result**: **QUALIFIED -- Ready for QA**
- **Recommendation**: Consider transitioning TC-9020 to ON_QA.

---

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status**: In Progress
- **Created**: 2026-05-10
- **Linked remediation Tasks (Depend)**:
  - TC-9024: Task, status **Done**
  - TC-9025: Task, status **In Progress**
- **Analysis**: TC-9024 is Done, but TC-9025 is still In Progress. At least one linked remediation Task is not yet complete.
- **Result**: **EXCLUDED -- remediation in progress**
- **Reason**: TC-9025 (In Progress) blocks QA readiness. This issue cannot move to ON_QA until all remediation Tasks reach Done or Closed status.

---

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status**: Modified
- **Created**: 2026-05-05
- **Linked remediation Tasks (Depend)**: None
- **Analysis**: The issue has no linked Tasks with link type "Depend". Without remediation Tasks, there is nothing to verify in QA.
- **Result**: **EXCLUDED -- no remediation to verify**
- **Reason**: No Depend-linked remediation Tasks exist. This issue may need remediation task creation before it can progress to QA. It could indicate that the issue was triaged but remediation was deferred, or that tasks were created without proper Depend linking.

## Summary

| Issue | CVE | Status | Depend Links | All Tasks Complete? | Ready for QA? |
|-------|-----|--------|--------------|---------------------|---------------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | No |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A | No |

**Total candidates**: 3
**Qualified for QA**: 1 (TC-9020)
**Excluded**: 2 (TC-9023 -- open task; TC-9026 -- no remediation tasks)
