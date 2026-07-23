# Ready for QA — Detailed Filtering Analysis

**Date**: 2026-07-23
**Project key**: TC

## Query

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

This query returns triaged Vulnerability issues that are not yet in a terminal or QA state. Each candidate is then evaluated based on its linked remediation Tasks (link type "Depend") to determine whether all remediation work is complete.

## Filtering Criteria

An issue qualifies as "Ready for QA" when:

1. It has the `ai-cve-triaged` label (confirmed triaged).
2. Its status is not Closed, Verified, or ON_QA (still actionable).
3. It has one or more linked Tasks with link type "Depend".
4. **ALL** of those linked Tasks have status Done or Closed.

An issue is **excluded** when:
- Any linked remediation Task is still open (status other than Done/Closed) -- remediation is in progress.
- No linked Tasks with link type "Depend" exist -- there is no remediation to verify.

## Candidate Analysis

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

| Field | Value |
|-------|-------|
| Issue key | TC-9020 |
| Status | Modified |
| CVE | CVE-2026-38901 |
| Summary | hyper - HTTP request smuggling [rhtpa-2.2] |
| Created | 2026-05-15 |
| Labels | CVE-2026-38901, pscomponent:org/rhtpa-server, ai-cve-triaged |

**Linked remediation Tasks (Depend):**

| Task | Type | Status | Completed? |
|------|------|--------|------------|
| TC-9021 | Task | Done | Yes |
| TC-9022 | Task | Closed | Yes |

**Result: QUALIFIED -- Ready for QA**

All linked remediation Tasks are completed (TC-9021 is Done, TC-9022 is Closed). This CVE has completed remediation and is a candidate for ON_QA transition.

**Recommendation**: Consider transitioning TC-9020 to ON_QA.

---

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

| Field | Value |
|-------|-------|
| Issue key | TC-9023 |
| Status | In Progress |
| CVE | CVE-2026-39102 |
| Summary | rustls - Certificate validation bypass [rhtpa-2.1] |
| Created | 2026-05-10 |
| Labels | CVE-2026-39102, pscomponent:org/rhtpa-server, ai-cve-triaged |

**Linked remediation Tasks (Depend):**

| Task | Type | Status | Completed? |
|------|------|--------|------------|
| TC-9024 | Task | Done | Yes |
| TC-9025 | Task | In Progress | No |

**Result: EXCLUDED -- Remediation in progress**

TC-9025 is still In Progress. Not all linked remediation Tasks are completed, so this issue cannot move to QA yet. Remediation work is still underway.

---

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

| Field | Value |
|-------|-------|
| Issue key | TC-9026 |
| Status | Modified |
| CVE | CVE-2026-39330 |
| Summary | openssl - Buffer overflow in X.509 parsing [rhtpa-2.2] |
| Created | 2026-05-05 |
| Labels | CVE-2026-39330, pscomponent:org/rhtpa-server, ai-cve-triaged |

**Linked remediation Tasks (Depend):** None

**Result: EXCLUDED -- No remediation to verify**

This issue has no linked Tasks with link type "Depend". Without remediation tasks, there is nothing to verify in QA. This issue may need remediation tasks created first, or it may have been closed/handled through a different mechanism.

---

## Summary

| Issue | CVE | Status | Depend Links | All Tasks Done? | Ready for QA? |
|-------|-----|--------|--------------|-----------------|---------------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | No -- remediation in progress |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A | No -- no remediation links |

**Total candidates evaluated**: 3
**Qualified for QA**: 1 (TC-9020)
**Excluded**: 2 (TC-9023 -- open task; TC-9026 -- no Depend links)
