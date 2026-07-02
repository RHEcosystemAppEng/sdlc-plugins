# Ready for QA — Filtering Analysis

## Overview

Query 3 searches for triaged CVE Vulnerability issues that are not yet closed, verified, or on QA:

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

3 candidate issues were returned. Each candidate's `issuelinks` field was inspected for linked Tasks with link type "Depend" to determine whether all remediation work is complete.

## Filtering Criteria

For a CVE to qualify as Ready for QA, it must satisfy all of the following:

1. The issue has at least one linked Task with link type "Depend".
2. Every such linked Task has a terminal status (Done or Closed).

If any linked Task is still open (any status other than Done or Closed), the CVE is excluded — remediation is still in progress.

If no linked Tasks with link type "Depend" exist, the CVE is excluded — there is no remediation work to verify.

## Candidate Analysis

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status:** Modified
- **Created:** 2026-05-15
- **Linked remediation Tasks (Depend):**
  - TC-9021 (Task) — **Done**
  - TC-9022 (Task) — **Closed**
- **Assessment:** ALL linked remediation Tasks are in a terminal status (Done or Closed).
- **Result: INCLUDED — Ready for QA**
- **Suggested action:** Consider transitioning TC-9020 to ON_QA.

---

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status:** In Progress
- **Created:** 2026-05-10
- **Linked remediation Tasks (Depend):**
  - TC-9024 (Task) — **Done**
  - TC-9025 (Task) — **In Progress**
- **Assessment:** TC-9025 is still In Progress. Not all remediation Tasks are complete.
- **Result: EXCLUDED — remediation incomplete**

---

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status:** Modified
- **Created:** 2026-05-05
- **Linked remediation Tasks (Depend):** (none)
- **Assessment:** No linked Tasks with link type "Depend" exist on this issue. Without remediation Tasks to verify, the issue cannot be confirmed as ready for QA.
- **Result: EXCLUDED — no remediation to verify**

## Summary

| Issue | CVE | Status | Depend Links | All Tasks Complete? | Ready for QA? |
|-------|-----|--------|--------------|---------------------|---------------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | No |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A | No |

**1 of 3 candidates qualified as Ready for QA: TC-9020.**
