# Ready for QA — Filtering Analysis

## Query

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

This query returns triaged Vulnerability issues that are not yet in a terminal or QA status. Each candidate is then evaluated by inspecting its linked remediation Tasks (link type "Depend") to determine if all remediation work is complete.

## Candidates Evaluated (3 issues)

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status**: Modified
- **Created**: 2026-05-15
- **Linked remediation Tasks (Depend)**:
  - TC-9021 (Task) — **Done**
  - TC-9022 (Task) — **Closed**
- **Assessment**: ALL linked remediation Tasks are in a completed status (Done or Closed).
- **Result**: **QUALIFIED — Ready for QA**
- **Recommendation**: Consider transitioning TC-9020 to ON_QA. All remediation work has been completed.

---

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status**: In Progress
- **Created**: 2026-05-10
- **Linked remediation Tasks (Depend)**:
  - TC-9024 (Task) — **Done**
  - TC-9025 (Task) — **In Progress**
- **Assessment**: TC-9025 is still In Progress. Not all linked remediation Tasks are complete.
- **Result**: **EXCLUDED — Remediation in progress**
- **Reason**: TC-9025 remains open (In Progress). The CVE cannot move to QA until all remediation tasks are completed.

---

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status**: Modified
- **Created**: 2026-05-05
- **Linked remediation Tasks (Depend)**: (none)
- **Assessment**: No linked Tasks with link type "Depend" exist on this issue.
- **Result**: **EXCLUDED — No remediation tasks to verify**
- **Reason**: Without linked remediation Tasks, there is no evidence that remediation work has been completed. The issue may need remediation tasks created or may require manual review.

---

## Summary

| Issue | CVE | Status | Linked Tasks | All Tasks Complete? | Ready for QA? |
|-------|-----|--------|--------------|---------------------|---------------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | No |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A | No |

**Result**: 1 of 3 candidates qualifies for QA transition: **TC-9020**.

### Filtering Rules Applied

1. **All linked remediation Tasks must be Done or Closed** — TC-9020 passes (2/2 tasks complete).
2. **Any linked Task still open causes exclusion** — TC-9023 excluded (TC-9025 still In Progress).
3. **No linked Tasks with type "Depend" causes exclusion** — TC-9026 excluded (no remediation tasks linked).
