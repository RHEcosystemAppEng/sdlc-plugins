# Ready for QA Filtering Analysis

## Overview

This analysis evaluates triaged Vulnerability issues to determine which have completed all remediation work and are candidates for ON_QA transition.

**Query used:**
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

**Candidates returned:** 3 issues

## Filtering Criteria

For each candidate, the linked issue relationships are inspected:

1. Extract all `issuelinks` entries where the link type name is "Depend"
2. For each linked Task, check its current status
3. Apply the qualification rules:
   - **Qualified** -- ALL linked remediation Tasks have status Done or Closed
   - **Excluded** -- ANY linked Task is still open (not Done or Closed)
   - **Excluded** -- NO linked Tasks with type "Depend" exist (no remediation to verify)

---

## Issue-by-Issue Analysis

### TC-9020 -- CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status:** Modified
- **CVE:** CVE-2026-38901
- **Created:** 2026-05-15

**Linked remediation Tasks (Depend type):**

| Linked Task | Type | Status | Completed? |
|-------------|------|--------|------------|
| TC-9021 | Task | Done | Yes |
| TC-9022 | Task | Closed | Yes |

**Assessment:** ALL linked remediation Tasks are in a completed state (Done or Closed).

**Result: QUALIFIED -- Ready for QA**

**Recommendation:** Consider transitioning TC-9020 to ON_QA. All remediation work has been completed.

---

### TC-9023 -- CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status:** In Progress
- **CVE:** CVE-2026-39102
- **Created:** 2026-05-10

**Linked remediation Tasks (Depend type):**

| Linked Task | Type | Status | Completed? |
|-------------|------|--------|------------|
| TC-9024 | Task | Done | Yes |
| TC-9025 | Task | In Progress | No |

**Assessment:** TC-9025 is still In Progress. Not all linked remediation Tasks are complete.

**Result: EXCLUDED -- Remediation in progress**

TC-9025 must reach Done or Closed status before this issue can be considered Ready for QA.

---

### TC-9026 -- CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status:** Modified
- **CVE:** CVE-2026-39330
- **Created:** 2026-05-05

**Linked remediation Tasks (Depend type):** None

**Assessment:** No linked Tasks with link type "Depend" were found on this issue. Without remediation tasks to verify, the issue cannot be moved to QA.

**Result: EXCLUDED -- No remediation to verify**

This issue may need investigation to determine whether remediation tasks were created under a different link type, or whether remediation has not yet been planned.

---

## Summary

| Issue | CVE | Status | Depend Links | All Tasks Done? | Ready for QA? |
|-------|-----|--------|--------------|-----------------|---------------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | No |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A | No |

**Final count:** 1 of 3 candidates qualified for Ready for QA transition.
