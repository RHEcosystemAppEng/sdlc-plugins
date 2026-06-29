# Ready for QA — Detailed Filtering Analysis

This document analyzes the Query 3 results to determine which triaged CVE issues are ready for QA transition.

## Query

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

3 candidate issues returned. Each is evaluated by inspecting its `issuelinks` for linked Tasks with link type "Depend".

---

## Filtering Criteria

For each candidate issue:
1. Check `issuelinks` for links where `type.name` is "Depend"
2. For each linked Task, check its current status
3. **Include** if ALL linked remediation Tasks are Done or Closed
4. **Exclude** if ANY linked Task is still open (not Done/Closed)
5. **Exclude** if there are NO linked Tasks with type "Depend" (no remediation to verify)

---

## Candidate Analysis

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status**: Modified
- **CVE**: CVE-2026-38901
- **Created**: 2026-05-15

**Linked remediation Tasks (Depend)**:

| Linked Task | Type | Status | Completed? |
|-------------|------|--------|------------|
| TC-9021 | Task | Done | Yes |
| TC-9022 | Task | Closed | Yes |

**Assessment**: ALL linked remediation Tasks are completed (Done or Closed).

**Result**: **INCLUDED** in Ready for QA

**Recommendation**: Consider transitioning TC-9020 to ON_QA. Both remediation tasks (TC-9021 and TC-9022) have been completed, and the vulnerability fix is ready for QA verification.

---

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status**: In Progress
- **CVE**: CVE-2026-39102
- **Created**: 2026-05-10

**Linked remediation Tasks (Depend)**:

| Linked Task | Type | Status | Completed? |
|-------------|------|--------|------------|
| TC-9024 | Task | Done | Yes |
| TC-9025 | Task | In Progress | No |

**Assessment**: TC-9025 is still In Progress. Not all remediation Tasks are complete.

**Result**: **EXCLUDED** — remediation is still in progress

**Reason**: TC-9025 remains In Progress, meaning the remediation work is not yet finished. This issue cannot move to ON_QA until all linked remediation Tasks reach Done or Closed status.

---

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status**: Modified
- **CVE**: CVE-2026-39330
- **Created**: 2026-05-05

**Linked remediation Tasks (Depend)**: None

**Assessment**: No issuelinks with type "Depend" exist on this issue.

**Result**: **EXCLUDED** — no remediation to verify

**Reason**: This issue has no linked remediation Tasks with the "Depend" link type. Without remediation Tasks to verify, there is nothing to move to QA. This may indicate that remediation tasks were not yet created, or that the issue was triaged with a different outcome (e.g., closed as not affected and later reopened).

---

## Summary

| Issue | CVE | Status | Depend Links | All Tasks Done? | Ready for QA? |
|-------|-----|--------|--------------|-----------------|---------------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | No |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A | No |

**1 of 3 candidates qualified for QA transition.**

### Action Items

- **TC-9020**: Transition to ON_QA. All remediation is complete.
- **TC-9023**: Monitor TC-9025 progress. Re-evaluate once TC-9025 reaches Done or Closed.
- **TC-9026**: Investigate why no Depend links exist. Remediation tasks may need to be created or linked.
