# Ready for QA — Detailed Filtering Analysis

## Overview

The Ready for QA query identifies triaged CVE Vulnerability issues whose remediation work is fully complete and are candidates for transitioning to ON_QA status.

**JQL Query**:
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

This query uses:
- **Project key**: `TC` (from Jira Configuration)
- **Vulnerability issue type ID**: `10024` (from Security Configuration)
- **Label filter**: `labels IN (ai-cve-triaged)` ensures only previously triaged issues are considered
- **Status exclusion**: `status NOT IN (Closed, Verified, 'ON_QA')` filters out issues that are already closed, verified, or already in QA — leaving only issues in a pre-QA state (e.g., Modified, In Progress, Assigned)

**Query returned 3 issues.** Each is evaluated below by inspecting its `issuelinks` for linked Tasks with link type "Depend" and fetching each linked Task's status.

---

## Issue-by-Issue Filtering

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status**: Modified
- **CVE**: CVE-2026-38901
- **Created**: 2026-05-15

**Linked remediation Tasks (Depend)**:

| Task Key | Issue Type | Status | Completed? |
|----------|-----------|--------|------------|
| TC-9021 | Task | Done | Yes |
| TC-9022 | Task | Closed | Yes |

**Evaluation**: ALL linked remediation Tasks are completed (Done or Closed).

**Result**: **INCLUDED** in Ready for QA.

**Recommendation**: Consider transitioning TC-9020 to ON_QA. All remediation work has been completed -- TC-9021 (Done) and TC-9022 (Closed) confirm that the fixes have been implemented and merged.

---

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status**: In Progress
- **CVE**: CVE-2026-39102
- **Created**: 2026-05-10

**Linked remediation Tasks (Depend)**:

| Task Key | Issue Type | Status | Completed? |
|----------|-----------|--------|------------|
| TC-9024 | Task | Done | Yes |
| TC-9025 | Task | In Progress | No |

**Evaluation**: NOT all linked remediation Tasks are completed. TC-9025 is still In Progress -- remediation is not yet complete.

**Result**: **EXCLUDED** from Ready for QA. Remediation task TC-9025 is still In Progress. The issue cannot transition to ON_QA until all linked remediation Tasks reach Done or Closed status.

---

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status**: Modified
- **CVE**: CVE-2026-39330
- **Created**: 2026-05-05

**Linked remediation Tasks (Depend)**: None.

**Evaluation**: No linked Tasks with link type "Depend" exist on this issue. Without linked remediation Tasks, there is no remediation work to verify.

**Result**: **EXCLUDED** from Ready for QA. No linked remediation Tasks with type "Depend" found -- there is no remediation to verify. This issue may need investigation: either remediation tasks were never created, or they were linked using a different link type.

---

## Summary

| Issue | Status | CVE | Ready for QA? | Reason |
|-------|--------|-----|---------------|--------|
| TC-9020 | Modified | CVE-2026-38901 | Yes | All remediation Tasks completed (TC-9021 Done, TC-9022 Closed) |
| TC-9023 | In Progress | CVE-2026-39102 | No | TC-9025 still In Progress |
| TC-9026 | Modified | CVE-2026-39330 | No | No Depend links (no remediation to verify) |

**Action items**:
- **TC-9020**: Suggest transitioning to ON_QA.
- **TC-9023**: Monitor TC-9025 progress. Re-evaluate when TC-9025 reaches Done or Closed.
- **TC-9026**: Investigate why no remediation Tasks are linked. May require re-triage or manual linking of existing remediation work.
