# Ready for QA — Detailed Filtering Analysis

## Query

**JQL**: `project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC`

This query finds triaged CVE Vulnerability issues (labeled `ai-cve-triaged`) that are still in a pre-QA state — i.e., not yet Closed, Verified, or ON_QA. The results are candidates for transitioning to ON_QA, but only if all their linked remediation Tasks are complete.

## Filtering Criteria

For each candidate issue returned by Query 3, inspect its `issuelinks` for linked Tasks with link type "Depend":

1. **ALL linked remediation Tasks are Done or Closed** -- include in Ready for QA. These CVEs have completed remediation and are candidates for ON_QA transition.
2. **ANY linked Task is still open** -- exclude. Remediation is still in progress.
3. **NO linked Tasks with type "Depend" exist** -- exclude. No remediation to verify.

---

## Issue-by-Issue Analysis

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status**: Modified
- **Labels**: CVE-2026-38901, pscomponent:org/rhtpa-server, ai-cve-triaged
- **Created**: 2026-05-15

**Linked Remediation Tasks (type: Depend):**

| Linked Task | Issue Type | Status | Complete? |
|-------------|-----------|--------|-----------|
| TC-9021 | Task | Done | Yes |
| TC-9022 | Task | Closed | Yes |

**Result: INCLUDED -- Ready for QA**

All linked remediation Tasks are completed (TC-9021 is Done, TC-9022 is Closed). Both statuses qualify as complete per the filtering criteria. This issue is a candidate for transitioning to ON_QA.

**Recommendation**: Consider transitioning TC-9020 to ON_QA.

---

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status**: In Progress
- **Labels**: CVE-2026-39102, pscomponent:org/rhtpa-server, ai-cve-triaged
- **Created**: 2026-05-10

**Linked Remediation Tasks (type: Depend):**

| Linked Task | Issue Type | Status | Complete? |
|-------------|-----------|--------|-----------|
| TC-9024 | Task | Done | Yes |
| TC-9025 | Task | In Progress | No |

**Result: EXCLUDED -- Remediation in progress**

TC-9025 is still In Progress. Not all linked remediation Tasks are complete. This issue cannot transition to ON_QA until TC-9025 reaches Done or Closed status.

---

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status**: Modified
- **Labels**: CVE-2026-39330, pscomponent:org/rhtpa-server, ai-cve-triaged
- **Created**: 2026-05-05

**Linked Remediation Tasks (type: Depend):**

No linked Tasks with link type "Depend" found.

**Result: EXCLUDED -- No remediation to verify**

Without any linked remediation Tasks of type "Depend", there is no completed remediation work to verify through QA. This issue cannot be transitioned to ON_QA until remediation Tasks are created and completed.

---

## Summary

| Issue | CVE | Status | Remediation Tasks | Ready for QA? | Reason |
|-------|-----|--------|-------------------|---------------|--------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | All tasks completed |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | TC-9025 still In Progress |
| TC-9026 | CVE-2026-39330 | Modified | (none) | No | No Depend-linked tasks |

**Qualified for ON_QA transition: 1 of 3 candidates**

- **TC-9020**: Consider transitioning to ON_QA. All remediation work (TC-9021, TC-9022) is complete.
