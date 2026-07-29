# Ready for QA — Detailed Filtering Analysis

**Project key:** TC
**Date:** 2026-07-29

## Overview

The Ready for QA query identifies triaged CVE Vulnerability issues whose remediation work is fully complete. These issues are candidates for transition to ON_QA status.

**Query used (Query 3):**
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

This query returned 3 candidate issues. Each candidate is evaluated by inspecting its `issuelinks` for linked Tasks with link type "Depend".

## Filtering Criteria

An issue qualifies as Ready for QA when **all** of the following are true:

1. The issue has at least one linked Task with link type "Depend"
2. Every such linked Task has a status of Done or Closed
3. No linked remediation Task is still open (any status other than Done/Closed)

An issue is excluded if:
- **Any linked Task is still open** -- remediation is still in progress
- **No linked Tasks with type "Depend" exist** -- there is no remediation to verify

## Candidate Analysis

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status:** Modified
- **CVE:** CVE-2026-38901
- **Created:** 2026-05-15
- **Linked remediation Tasks (Depend):**
  - TC-9021 (Task) — **Done**
  - TC-9022 (Task) — **Closed**
- **Assessment:** ALL linked remediation Tasks are in a completed state (Done or Closed).
- **Result: QUALIFIED — Ready for QA**
- **Recommendation:** Consider transitioning TC-9020 to ON_QA.

---

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status:** In Progress
- **CVE:** CVE-2026-39102
- **Created:** 2026-05-10
- **Linked remediation Tasks (Depend):**
  - TC-9024 (Task) — **Done**
  - TC-9025 (Task) — **In Progress**
- **Assessment:** TC-9025 is still In Progress. Not all remediation Tasks are completed.
- **Result: EXCLUDED — remediation in progress**
- **Reason:** TC-9025 remains in "In Progress" status. Until all linked remediation Tasks reach Done or Closed, this issue cannot be considered Ready for QA.

---

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status:** Modified
- **CVE:** CVE-2026-39330
- **Created:** 2026-05-05
- **Linked remediation Tasks (Depend):** None
- **Assessment:** No linked Tasks with link type "Depend" exist on this issue.
- **Result: EXCLUDED — no remediation to verify**
- **Reason:** Without any linked remediation Tasks, there is no completed remediation work to verify in QA. This issue may need investigation — it could be missing remediation task links, or remediation may not have been created yet.

---

## Summary

| Issue | CVE | Status | Linked Tasks | All Tasks Complete? | Ready for QA? |
|-------|-----|--------|--------------|---------------------|---------------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | No — open task |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A | No — no Depend links |

**Qualified for QA transition:** 1 of 3 candidates (TC-9020)
