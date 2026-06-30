# Ready for QA — Detailed Filtering Analysis

This document provides the detailed analysis of Query 3 (Ready for QA candidates) from the discovery mode run. It explains the filtering logic applied to each candidate issue and the rationale for inclusion or exclusion.

## Filtering Criteria

Per the triage-security skill (SKILL.md, Discovery Mode, Query 3):

1. Search for triaged Vulnerability issues that are not yet Closed, Verified, or ON_QA.
2. For each result, inspect `issuelinks` for linked Tasks with link type "Depend".
3. Apply the following rules:
   - **ALL linked remediation Tasks are Done or Closed** --> include in "Ready for QA" list. These CVEs have completed remediation and are candidates for ON_QA transition.
   - **ANY linked Task is still open** --> exclude. Remediation is still in progress.
   - **NO linked Tasks with type "Depend" exist** --> exclude. No remediation to verify.

## JQL Query

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

Fields requested: summary, labels, status, created, issuelinks

## Candidate Issues (3 returned)

---

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status:** Modified
- **Labels:** CVE-2026-38901, pscomponent:org/rhtpa-server, ai-cve-triaged
- **Created:** 2026-05-15

**Linked remediation Tasks (Depend):**

| Linked Task | Issue Type | Status | Completed? |
|-------------|-----------|--------|------------|
| TC-9021 | Task | Done | Yes |
| TC-9022 | Task | Closed | Yes |

**Analysis:** Both linked remediation Tasks have terminal statuses (Done and Closed). All remediation work is complete.

**Result: QUALIFIED — Ready for QA**

**Proposed action:** Transition TC-9020 to ON_QA. All linked remediation tasks are complete — the CVE fix is ready for verification testing.

---

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status:** In Progress
- **Labels:** CVE-2026-39102, pscomponent:org/rhtpa-server, ai-cve-triaged
- **Created:** 2026-05-10

**Linked remediation Tasks (Depend):**

| Linked Task | Issue Type | Status | Completed? |
|-------------|-----------|--------|------------|
| TC-9024 | Task | Done | Yes |
| TC-9025 | Task | In Progress | No |

**Analysis:** TC-9024 is Done (completed), but TC-9025 is still In Progress (open). Because at least one linked remediation Task is not in a terminal status, this issue does not qualify. Remediation is still in progress.

**Result: EXCLUDED — Remediation in progress**

**Reason:** TC-9025 remains In Progress. The issue cannot move to QA until all linked remediation Tasks reach Done or Closed status.

---

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status:** Modified
- **Labels:** CVE-2026-39330, pscomponent:org/rhtpa-server, ai-cve-triaged
- **Created:** 2026-05-05

**Linked remediation Tasks (Depend):**

None. This issue has no `issuelinks` entries with link type "Depend".

**Analysis:** With no linked remediation Tasks, there is no remediation work to verify. The issue cannot be moved to QA because there is nothing to test. This may indicate that:
- Remediation tasks were never created (triage may have been incomplete)
- The issue was triaged as "not affected" but not yet closed
- Remediation tasks exist but are not properly linked

**Result: EXCLUDED — No remediation to verify**

**Reason:** No linked Tasks with type "Depend" exist. The Ready for QA filter requires at least one linked remediation Task, and all such tasks must be completed.

---

## Summary

| Issue | CVE | Status | Linked Tasks | All Complete? | Ready for QA? |
|-------|-----|--------|--------------|---------------|---------------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | No — open task |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A | No — no Depend links |

**Final Ready for QA list:** 1 issue (TC-9020)

**Proposed actions:**
- **TC-9020:** Consider transitioning to ON_QA. All remediation tasks (TC-9021, TC-9022) are complete.
- **TC-9023:** No action — wait for TC-9025 to complete before re-evaluating.
- **TC-9026:** Investigate why no remediation tasks are linked. May need follow-up triage or manual linking.
