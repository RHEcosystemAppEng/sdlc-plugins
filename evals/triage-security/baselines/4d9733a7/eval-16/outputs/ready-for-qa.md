# Ready for QA -- Detailed Filtering Analysis

## Query 3 Results Processing

The third JQL query finds triaged CVEs that are still in a pre-QA state:

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

This query returns 3 issues. For each, the skill inspects `issuelinks` for linked Tasks with link type "Depend" and fetches each linked Task's status.

---

## TC-9020 -- CVE-2026-38901 (hyper - HTTP request smuggling [rhtpa-2.2])

**Status**: Modified
**Issue Links (Depend type)**:
- TC-9021 (Task) -- Status: **Done**
- TC-9022 (Task) -- Status: **Closed**

**Analysis**: ALL linked remediation Tasks are completed:
- TC-9021: Done (completed)
- TC-9022: Closed (completed)

**Result**: **INCLUDED in Ready for QA**

**Recommendation**: Consider transitioning TC-9020 to ON_QA. All remediation work is complete and ready for quality assurance verification.

---

## TC-9023 -- CVE-2026-39102 (rustls - Certificate validation bypass [rhtpa-2.1])

**Status**: In Progress
**Issue Links (Depend type)**:
- TC-9024 (Task) -- Status: **Done**
- TC-9025 (Task) -- Status: **In Progress**

**Analysis**: Not all linked remediation Tasks are completed:
- TC-9024: Done (completed)
- TC-9025: **In Progress** (still open -- remediation not complete)

**Result**: **EXCLUDED from Ready for QA** -- TC-9025 is still In Progress. Remediation is not complete.

---

## TC-9026 -- CVE-2026-39330 (openssl - Buffer overflow in X.509 parsing [rhtpa-2.2])

**Status**: Modified
**Issue Links (Depend type)**: None

**Analysis**: No linked Tasks with type "Depend" found. Without remediation tasks to verify, this issue cannot be evaluated for QA readiness.

**Result**: **EXCLUDED from Ready for QA** -- No linked remediation tasks with type "Depend". No remediation to verify.

---

## Summary

| Issue | Linked Tasks | All Complete? | Ready for QA? | Reason |
|-------|-------------|---------------|---------------|--------|
| TC-9020 | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes | All remediation tasks completed |
| TC-9023 | TC-9024 (Done), TC-9025 (In Progress) | No | No | TC-9025 still In Progress |
| TC-9026 | (none) | N/A | No | No Depend links -- no remediation to verify |

### Ready for QA Table

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

For TC-9020: Consider transitioning to ON_QA.
