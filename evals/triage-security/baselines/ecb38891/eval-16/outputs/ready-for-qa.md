# Ready for QA — Detailed Filtering Analysis

## JQL Query

The Ready for QA query is constructed using the project key (TC) and vulnerability issue type ID (10024) extracted from the Security Configuration:

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

This query returns triaged CVEs (marked with `ai-cve-triaged` label) that are still in a pre-QA state — not yet transitioned to Closed, Verified, or ON_QA. These are candidates to check for completed remediation.

## Filtering Protocol

For each result returned by the query, the following checks are performed:

1. Inspect the issue's `issuelinks` array for linked issues where `type.name` is `"Depend"`.
2. For each Depend link, extract the linked issue key (from `outwardIssue.key` or `inwardIssue.key`) and fetch the linked issue to check its status.
3. Apply the decision rules:
   - **ALL linked remediation Tasks are Done or Closed** --> include in Ready for QA list.
   - **ANY linked Task is still open** (not Done or Closed) --> exclude. Remediation still in progress.
   - **NO linked Tasks with type "Depend" exist** --> exclude. No remediation to verify.

## Issue-by-Issue Analysis

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status**: Modified
- **CVE**: CVE-2026-38901
- **Created**: 2026-05-15

**Linked remediation Tasks (Depend):**

| Task Key | Issue Type | Status | Completed? |
|----------|-----------|--------|------------|
| TC-9021 | Task | Done | Yes |
| TC-9022 | Task | Closed | Yes |

**Decision**: ALL linked remediation Tasks are completed (TC-9021 is Done, TC-9022 is Closed).

**Result**: **INCLUDED** in Ready for QA. All remediation work is complete.

**Recommendation**: Consider transitioning TC-9020 to ON_QA.

---

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status**: In Progress
- **CVE**: CVE-2026-39102
- **Created**: 2026-05-10

**Linked remediation Tasks (Depend):**

| Task Key | Issue Type | Status | Completed? |
|----------|-----------|--------|------------|
| TC-9024 | Task | Done | Yes |
| TC-9025 | Task | In Progress | No |

**Decision**: NOT all linked remediation Tasks are completed. TC-9025 is still In Progress — remediation is not yet complete.

**Result**: **EXCLUDED** from Ready for QA. Reason: TC-9025 is still In Progress. The CVE cannot move to ON_QA until all remediation tasks are finished.

---

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status**: Modified
- **CVE**: CVE-2026-39330
- **Created**: 2026-05-05

**Linked remediation Tasks (Depend):**

No linked Tasks with type "Depend" found on this issue.

**Decision**: No remediation tasks exist to verify completion against. Without Depend-linked tasks, there is no evidence of remediation work to validate for QA.

**Result**: **EXCLUDED** from Ready for QA. Reason: No linked Tasks with type "Depend". No remediation to verify.

---

## Summary

| Issue | CVE | Status | Linked Tasks | All Complete? | Ready for QA? | Reason |
|-------|-----|--------|--------------|---------------|---------------|--------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes | All remediation Tasks completed |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | No | TC-9025 still In Progress |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A | No | No Depend links — no remediation to verify |

## Qualified for ON_QA Transition

Only **TC-9020** qualifies for the ON_QA transition. Proposed action:

- Transition TC-9020 from Modified to ON_QA.
- All linked remediation tasks (TC-9021 and TC-9022) have been completed, confirming that the fix for CVE-2026-38901 has been delivered.
