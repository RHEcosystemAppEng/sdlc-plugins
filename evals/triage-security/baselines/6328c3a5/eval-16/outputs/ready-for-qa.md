# Ready for QA — Filtering Analysis

## Overview

Query 3 searches for triaged Vulnerability issues that are not yet Closed, Verified, or ON_QA. These are candidates whose remediation work may be complete, making them eligible for QA transition.

**JQL used:**
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

**Results returned:** 3 issues

---

## Filtering Criteria

For each candidate, the filtering logic inspects `issuelinks` for linked Tasks with link type "Depend":

1. **ALL linked remediation Tasks are Done or Closed** -- include in Ready for QA list. These CVEs have completed remediation and are candidates for ON_QA transition.
2. **ANY linked Task is still open** -- exclude. Remediation is still in progress.
3. **NO linked Tasks with type "Depend" exist** -- exclude. No remediation to verify.

---

## Issue-by-Issue Analysis

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status:** Modified
- **CVE:** CVE-2026-38901
- **Created:** 2026-05-15
- **Depend links:**
  - TC-9021 (Task) — Status: **Done**
  - TC-9022 (Task) — Status: **Closed**
- **Assessment:** Both linked remediation Tasks have terminal statuses (Done and Closed). All remediation work is complete.
- **Result: QUALIFIED — Ready for QA**
- **Recommendation:** Consider transitioning TC-9020 to ON_QA.

---

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status:** In Progress
- **CVE:** CVE-2026-39102
- **Created:** 2026-05-10
- **Depend links:**
  - TC-9024 (Task) — Status: **Done**
  - TC-9025 (Task) — Status: **In Progress**
- **Assessment:** TC-9025 is still In Progress. Not all linked remediation Tasks are complete.
- **Result: EXCLUDED — remediation in progress**
- **Reason:** TC-9025 remains open (In Progress). The CVE cannot move to QA until all remediation Tasks reach Done or Closed status.

---

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status:** Modified
- **CVE:** CVE-2026-39330
- **Created:** 2026-05-05
- **Depend links:** (none)
- **Assessment:** No linked Tasks with link type "Depend" exist on this issue.
- **Result: EXCLUDED — no remediation to verify**
- **Reason:** Without Depend-linked remediation Tasks, there is no remediation work to verify. This issue may need remediation tasks created before it can proceed to QA, or it may have been triaged as not requiring remediation (in which case it should have been closed, not left in Modified status).

---

## Summary

| Issue | CVE | Status | Depend Links | All Tasks Complete? | Ready for QA? |
|-------|-----|--------|--------------|---------------------|---------------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | No |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A | No |

**Qualified for QA transition:** 1 of 3 candidates (TC-9020)
**Excluded:** 2 of 3 candidates (TC-9023 has open remediation; TC-9026 has no remediation links)
