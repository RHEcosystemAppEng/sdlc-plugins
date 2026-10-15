# Ready for QA — Filtering Analysis

**Project key:** TC
**Date:** 2026-10-15

## Query

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

This query returns triaged Vulnerability issues that have not yet reached ON_QA, Verified, or Closed status. Each result is then evaluated to determine whether all linked remediation Tasks are complete.

## Candidate Issues

3 candidate issues returned by the query.

---

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status:** Modified
- **Labels:** CVE-2026-38901, pscomponent:org/rhtpa-server, ai-cve-triaged
- **Created:** 2026-05-15

**Linked remediation Tasks (Depend):**

| Linked Task | Issue Type | Status | Complete? |
|-------------|-----------|--------|-----------|
| TC-9021 | Task | Done | Yes |
| TC-9022 | Task | Closed | Yes |

**Evaluation:** ALL linked remediation Tasks have a terminal status (Done or Closed). Both TC-9021 and TC-9022 are complete.

**Result: QUALIFIED — Ready for QA**

Recommended action: Transition TC-9020 to ON_QA. All remediation work is complete and the fixes are ready for verification.

---

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status:** In Progress
- **Labels:** CVE-2026-39102, pscomponent:org/rhtpa-server, ai-cve-triaged
- **Created:** 2026-05-10

**Linked remediation Tasks (Depend):**

| Linked Task | Issue Type | Status | Complete? |
|-------------|-----------|--------|-----------|
| TC-9024 | Task | Done | Yes |
| TC-9025 | Task | In Progress | No |

**Evaluation:** TC-9025 is still In Progress. Not all remediation Tasks are complete. The issue cannot move to ON_QA until TC-9025 reaches Done or Closed.

**Result: EXCLUDED — Remediation in progress**

Reason: At least one linked remediation Task (TC-9025) has a non-terminal status. Remediation work is still active.

---

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status:** Modified
- **Labels:** CVE-2026-39330, pscomponent:org/rhtpa-server, ai-cve-triaged
- **Created:** 2026-05-05

**Linked remediation Tasks (Depend):**

No linked issues with link type "Depend" found.

**Evaluation:** Without any linked remediation Tasks, there is no completed remediation work to verify. The issue cannot be promoted to ON_QA because there are no Tasks to confirm the fix.

**Result: EXCLUDED — No remediation to verify**

Reason: No linked Tasks with link type "Depend" exist on this issue. Either remediation Tasks were never created, or they were linked with a different link type.

---

## Summary

| Issue | CVE | Status | Depend Links | All Tasks Complete? | Ready for QA? |
|-------|-----|--------|-------------|---------------------|---------------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | No |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A | No |

**Qualified for ON_QA transition:** 1 of 3 candidates (TC-9020)

### Filtering Rules Applied

1. **ALL linked remediation Tasks must be Done or Closed** — A single open Task disqualifies the issue. Both "Done" and "Closed" are accepted as terminal/complete statuses.
2. **ANY linked Task still open** — The issue is excluded. Remediation is still in progress and cannot be verified yet.
3. **NO linked Tasks with type "Depend"** — The issue is excluded. Without remediation Tasks to verify, there is no basis for QA transition.
