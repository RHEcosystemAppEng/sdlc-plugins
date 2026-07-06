# Ready for QA — Filtering Analysis

**Project**: TC | **Date**: 2026-07-06

## Query

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

This query returns triaged Vulnerability issues that are not yet in a terminal or QA state. Each result is then evaluated by inspecting its `issuelinks` for linked Tasks with link type "Depend" to determine whether all remediation work is complete.

## Filtering Criteria

An issue qualifies as "Ready for QA" only when **all** of these conditions hold:

1. The issue has at least one linked Task with link type "Depend"
2. Every such linked Task has status Done or Closed

An issue is excluded if:
- Any linked remediation Task is still open (not Done/Closed)
- No linked Tasks with link type "Depend" exist (no remediation to verify)

## Candidate Evaluation

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status**: Modified
- **CVE**: CVE-2026-38901
- **Linked remediation Tasks**:
  - TC-9021 (Task) — **Done**
  - TC-9022 (Task) — **Closed**
- **Assessment**: ALL linked remediation Tasks are in a completed state (Done or Closed)
- **Result**: **INCLUDED** — Ready for QA
- **Recommendation**: Consider transitioning TC-9020 to ON_QA. All remediation work has been completed and the issue is ready for verification.

---

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status**: In Progress
- **CVE**: CVE-2026-39102
- **Linked remediation Tasks**:
  - TC-9024 (Task) — **Done**
  - TC-9025 (Task) — **In Progress**
- **Assessment**: TC-9025 is still In Progress. Not all remediation Tasks are complete.
- **Result**: **EXCLUDED** — Remediation is still in progress

---

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status**: Modified
- **CVE**: CVE-2026-39330
- **Linked remediation Tasks**: (none with link type "Depend")
- **Assessment**: No linked Tasks with type "Depend" exist. There is no remediation work to verify.
- **Result**: **EXCLUDED** — No remediation to verify

---

## Summary

| Issue | CVE | Status | Depend Links | All Tasks Complete? | Ready for QA? |
|-------|-----|--------|--------------|---------------------|---------------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | No |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A | No |

**1 of 3 candidates qualified for Ready for QA transition.**

### Action Items

- **TC-9020**: Transition to ON_QA — all remediation tasks (TC-9021, TC-9022) are complete.
