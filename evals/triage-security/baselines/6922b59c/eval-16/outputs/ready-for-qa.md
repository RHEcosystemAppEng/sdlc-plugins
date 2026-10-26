# Ready for QA — Filtering Analysis

## Query

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

This query returns triaged Vulnerability issues that are not yet Closed, Verified, or ON_QA. Each candidate is then evaluated by inspecting its `issuelinks` for linked Tasks with link type "Depend" to determine whether all remediation work is complete.

## Candidates Evaluated (3)

---

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status:** Modified
- **Labels:** CVE-2026-38901, pscomponent:org/rhtpa-server, ai-cve-triaged
- **Created:** 2026-05-15

**Linked remediation Tasks (Depend):**

| Linked Task | Type | Status |
|-------------|------|--------|
| TC-9021 | Task | Done |
| TC-9022 | Task | Closed |

**Analysis:** All linked remediation Tasks are in a terminal state (Done or Closed). Both TC-9021 and TC-9022 have completed their remediation work.

**Result: QUALIFIED — Ready for QA**

Reason: All 2 linked remediation Tasks with link type "Depend" are completed (Done or Closed). This CVE has completed remediation and is a candidate for ON_QA transition.

---

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status:** In Progress
- **Labels:** CVE-2026-39102, pscomponent:org/rhtpa-server, ai-cve-triaged
- **Created:** 2026-05-10

**Linked remediation Tasks (Depend):**

| Linked Task | Type | Status |
|-------------|------|--------|
| TC-9024 | Task | Done |
| TC-9025 | Task | In Progress |

**Analysis:** TC-9024 is Done, but TC-9025 is still In Progress. Not all linked remediation Tasks have reached a terminal state.

**Result: EXCLUDED — Remediation in progress**

Reason: TC-9025 is still In Progress. At least one linked remediation Task is open, so this CVE is not ready for QA. Remediation work is still underway.

---

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status:** Modified
- **Labels:** CVE-2026-39330, pscomponent:org/rhtpa-server, ai-cve-triaged
- **Created:** 2026-05-05

**Linked remediation Tasks (Depend):**

(none)

**Analysis:** This issue has no linked Tasks with link type "Depend". Without remediation task links, there is no verifiable remediation work to confirm as complete.

**Result: EXCLUDED — No remediation tasks to verify**

Reason: No linked Tasks with type "Depend" exist on this issue. Without linked remediation Tasks, the issue cannot be confirmed as having completed remediation. It may need remediation tasks created, or its remediation may be tracked differently.

---

## Filtering Summary

| Issue | CVE | Status | Depend Links | All Complete? | Ready for QA? |
|-------|-----|--------|--------------|---------------|---------------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | No — open task |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A | No — no tasks |

## Filtering Rules Applied

1. **ALL linked remediation Tasks are Done or Closed** -- include in Ready for QA list. These CVEs have completed remediation and are candidates for ON_QA transition.
2. **ANY linked Task is still open** -- exclude. Remediation is still in progress.
3. **NO linked Tasks with type "Depend" exist** -- exclude. No remediation to verify.

## Result

**1 of 3 candidates qualified for Ready for QA: TC-9020**

Recommendation: Consider transitioning TC-9020 to ON_QA.
