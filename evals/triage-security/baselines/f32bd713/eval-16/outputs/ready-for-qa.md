# Ready for QA Filtering Analysis

## Overview

This analysis evaluates triaged CVE Vulnerability issues to determine which are candidates for transition to ON_QA status. A CVE is Ready for QA when **all** of its linked remediation Tasks (linked via "Depend" link type) have reached a terminal status (Done or Closed).

**Query used:**
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

**Candidates returned:** 3 issues

---

## Filtering Criteria

For each candidate, the following rules are applied per the skill definition:

1. Inspect `issuelinks` for linked Tasks with link type "Depend".
2. **ALL linked remediation Tasks are Done or Closed** --> include in Ready for QA list.
3. **ANY linked Task is still open** --> exclude (remediation still in progress).
4. **NO linked Tasks with type "Depend" exist** --> exclude (no remediation to verify).

---

## Issue-by-Issue Analysis

### TC-9020 -- CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status:** Modified
- **CVE:** CVE-2026-38901
- **Created:** 2026-05-15

**Linked remediation Tasks (Depend):**

| Linked Task | Type | Status | Terminal? |
|-------------|------|--------|-----------|
| TC-9021 | Task | Done | Yes |
| TC-9022 | Task | Closed | Yes |

**Evaluation:** ALL linked remediation Tasks have reached a terminal status (Done or Closed). There are no open or in-progress Tasks blocking this CVE.

**Result: QUALIFIED -- Ready for QA**

> Recommendation: Consider transitioning TC-9020 to ON_QA.

---

### TC-9023 -- CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status:** In Progress
- **CVE:** CVE-2026-39102
- **Created:** 2026-05-10

**Linked remediation Tasks (Depend):**

| Linked Task | Type | Status | Terminal? |
|-------------|------|--------|-----------|
| TC-9024 | Task | Done | Yes |
| TC-9025 | Task | In Progress | No |

**Evaluation:** TC-9025 is still In Progress. Not all linked remediation Tasks have reached a terminal status. Remediation work is still underway.

**Result: EXCLUDED -- remediation in progress (TC-9025 In Progress)**

---

### TC-9026 -- CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status:** Modified
- **CVE:** CVE-2026-39330
- **Created:** 2026-05-05

**Linked remediation Tasks (Depend):**

(none)

**Evaluation:** No linked Tasks with link type "Depend" were found on this issue. Without remediation Tasks to verify, this CVE cannot be moved to QA. It may be missing remediation task creation, or the tasks may have been linked with a different link type.

**Result: EXCLUDED -- no Depend-linked remediation Tasks to verify**

---

## Summary

| Issue | CVE | Status | Depend-Linked Tasks | All Tasks Done/Closed? | Ready for QA? |
|-------|-----|--------|---------------------|------------------------|---------------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | No |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A | No |

**Qualified for QA transition:** 1 of 3 candidates (TC-9020)
