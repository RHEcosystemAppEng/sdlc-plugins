# Ready for QA Filtering Analysis

## Overview

Query 3 searches for triaged CVEs that are not yet Closed, Verified, or ON_QA, then inspects their linked remediation tasks to determine which issues have completed all remediation and are candidates for ON_QA transition.

**JQL used:**
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

**Candidates returned:** 3 issues

---

## Filtering Criteria

For each candidate issue, the filtering logic inspects `issuelinks` for linked Tasks with link type "Depend":

1. **ALL linked remediation Tasks are Done or Closed** --> include in Ready for QA list
2. **ANY linked Task is still open** --> exclude (remediation in progress)
3. **NO linked Tasks with type "Depend" exist** --> exclude (no remediation to verify)

---

## Per-Issue Analysis

### TC-9020 -- CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status:** Modified
- **CVE:** CVE-2026-38901
- **Created:** 2026-05-15

**Linked remediation tasks (Depend):**

| Linked Task | Type | Status | Completed? |
|-------------|------|--------|------------|
| TC-9021 | Task | Done | Yes |
| TC-9022 | Task | Closed | Yes |

**Evaluation:** ALL linked remediation Tasks are in a completed state (Done or Closed).

**Result: QUALIFIED -- Ready for QA**

Recommendation: Consider transitioning TC-9020 to ON_QA.

---

### TC-9023 -- CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status:** In Progress
- **CVE:** CVE-2026-39102
- **Created:** 2026-05-10

**Linked remediation tasks (Depend):**

| Linked Task | Type | Status | Completed? |
|-------------|------|--------|------------|
| TC-9024 | Task | Done | Yes |
| TC-9025 | Task | In Progress | No |

**Evaluation:** TC-9025 is still In Progress. Not all linked remediation Tasks are completed.

**Result: EXCLUDED -- remediation in progress**

TC-9025 must reach Done or Closed status before TC-9023 can be considered Ready for QA.

---

### TC-9026 -- CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status:** Modified
- **CVE:** CVE-2026-39330
- **Created:** 2026-05-05

**Linked remediation tasks (Depend):** None

**Evaluation:** No linked Tasks with link type "Depend" exist on this issue. Without remediation tasks to verify, the issue cannot be determined Ready for QA.

**Result: EXCLUDED -- no remediation tasks to verify**

This issue may need remediation tasks created (re-triage or manual task creation) before it can progress to QA.

---

## Summary

| Issue | CVE | Status | Depend Links | All Tasks Done? | Ready for QA? |
|-------|-----|--------|--------------|-----------------|---------------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | No |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A | No |

**1 of 3 candidates qualified for ON_QA transition: TC-9020.**
