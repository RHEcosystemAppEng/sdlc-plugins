# Ready for QA — Filtering Analysis

## Overview

Query 3 identifies triaged CVEs that may be ready for QA verification. The JQL query returns Vulnerability issues with the `ai-cve-triaged` label whose status is not yet Closed, Verified, or ON_QA:

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

3 candidate issues were returned. Each must pass the Depend-link remediation check to qualify as Ready for QA.

---

## Filtering Criteria

For each candidate issue, the `issuelinks` field is inspected for linked Tasks with link type "Depend":

1. **ALL linked remediation Tasks are Done or Closed** -- the issue qualifies as Ready for QA. All remediation work is complete and the CVE is a candidate for ON_QA transition.
2. **ANY linked Task is still open** (not Done or Closed) -- the issue is excluded. Remediation is still in progress.
3. **NO linked Tasks with type "Depend" exist** -- the issue is excluded. There is no remediation work to verify.

---

## Per-Issue Analysis

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status**: Modified
- **CVE**: CVE-2026-38901
- **Created**: 2026-05-15
- **Depend-linked Tasks**:
  - TC-9021 — Status: **Done**
  - TC-9022 — Status: **Closed**
- **Assessment**: ALL linked remediation Tasks are in a completed state (Done or Closed). No open tasks remain.
- **Result**: **QUALIFIED -- Ready for QA**
- **Recommendation**: Consider transitioning TC-9020 to ON_QA. All remediation tasks have been completed and the fixes are ready for verification.

---

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status**: In Progress
- **CVE**: CVE-2026-39102
- **Created**: 2026-05-10
- **Depend-linked Tasks**:
  - TC-9024 — Status: **Done**
  - TC-9025 — Status: **In Progress**
- **Assessment**: TC-9025 is still In Progress. Not all remediation Tasks are complete.
- **Result**: **EXCLUDED -- remediation in progress**
- **Reason**: TC-9025 (In Progress) has not yet reached Done or Closed status. Until all Depend-linked Tasks are completed, this CVE cannot move to QA verification.

---

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status**: Modified
- **CVE**: CVE-2026-39330
- **Created**: 2026-05-05
- **Depend-linked Tasks**: (none)
- **Assessment**: No issuelinks with link type "Depend" were found on this issue. Without linked remediation Tasks, there is no completed work to verify.
- **Result**: **EXCLUDED -- no remediation to verify**
- **Reason**: An issue with no Depend links has no tracked remediation work. It may need re-triage to create remediation tasks, or the remediation may have been handled outside of the standard workflow.

---

## Summary

| Issue | CVE | Status | Depend-linked Tasks | All Tasks Complete? | Ready for QA? |
|-------|-----|--------|---------------------|---------------------|---------------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes -- suggest ON_QA transition |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | No -- TC-9025 still open |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A | No -- no Depend links |

**1 of 3 candidates qualified for Ready for QA: TC-9020.**
