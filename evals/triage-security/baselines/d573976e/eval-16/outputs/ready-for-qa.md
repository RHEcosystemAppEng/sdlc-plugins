# Ready for QA — Detailed Filtering Analysis

## Overview

The third JQL query identifies triaged CVEs (with `ai-cve-triaged` label) that are still in a pre-QA state. The goal is to find CVEs where all remediation work is complete and the issue is ready to transition to ON_QA.

**JQL:**
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

This query uses:
- **Project key**: TC (from Jira Configuration)
- **Issue type ID**: 10024 (Vulnerability issue type from Security Configuration)
- **Label filter**: `ai-cve-triaged` — only issues that have already been triaged
- **Status exclusion**: Closed, Verified, ON_QA — excludes issues already past the QA gate

The query returned **3 candidate issues**. Each must be evaluated by inspecting its `issuelinks` array for linked Tasks with link type "Depend" and checking whether ALL such tasks are Done or Closed.

---

## Filtering Criteria

Per the discovery mode protocol, a candidate qualifies for Ready for QA only if:
1. It has linked Tasks with link type "Depend" (remediation tasks exist)
2. **ALL** linked remediation Tasks are Done or Closed (remediation is complete)

A candidate is excluded if:
- **ANY** linked Task is still open (remediation in progress)
- **NO** linked Tasks with type "Depend" exist (no remediation to verify)

---

## Issue-by-Issue Analysis

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

**Status:** Modified
**Created:** 2026-05-15
**Labels:** CVE-2026-38901, pscomponent:org/rhtpa-server, ai-cve-triaged

**Linked remediation Tasks (type: Depend):**

| Task | Type | Status | Complete? |
|------|------|--------|-----------|
| TC-9021 | Task | Done | Yes |
| TC-9022 | Task | Closed | Yes |

**Assessment:** ALL linked remediation Tasks are completed.
- TC-9021: **Done** (completed)
- TC-9022: **Closed** (completed)

**Result: INCLUDED in Ready for QA.**

**Recommendation:** Consider transitioning TC-9020 to **ON_QA**. All remediation tasks have been completed and the CVE fix is ready for QA verification.

---

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

**Status:** In Progress
**Created:** 2026-05-10
**Labels:** CVE-2026-39102, pscomponent:org/rhtpa-server, ai-cve-triaged

**Linked remediation Tasks (type: Depend):**

| Task | Type | Status | Complete? |
|------|------|--------|-----------|
| TC-9024 | Task | Done | Yes |
| TC-9025 | Task | In Progress | No |

**Assessment:** NOT all linked remediation Tasks are completed.
- TC-9024: **Done** (completed)
- TC-9025: **In Progress** (still open — remediation is not yet complete)

**Result: EXCLUDED from Ready for QA.** Remediation is still in progress. TC-9025 must reach Done or Closed status before this CVE can transition to ON_QA.

---

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

**Status:** Modified
**Created:** 2026-05-05
**Labels:** CVE-2026-39330, pscomponent:org/rhtpa-server, ai-cve-triaged

**Linked remediation Tasks (type: Depend):** None.

The issue has no linked Tasks with link type "Depend". There are no remediation tasks to verify — either remediation was handled outside the standard workflow, or tasks were never created.

**Result: EXCLUDED from Ready for QA.** No linked remediation Tasks with type "Depend" exist. There is no remediation to verify for QA readiness.

---

## Summary

| Issue | Status | CVE | Depend Links | All Tasks Done? | Ready for QA? | Reason |
|-------|--------|-----|-------------|-----------------|---------------|--------|
| TC-9020 | Modified | CVE-2026-38901 | TC-9021 (Done), TC-9022 (Closed) | Yes | **Yes** | All remediation complete |
| TC-9023 | In Progress | CVE-2026-39102 | TC-9024 (Done), TC-9025 (In Progress) | No | **No** | TC-9025 still In Progress |
| TC-9026 | Modified | CVE-2026-39330 | (none) | N/A | **No** | No Depend links — no remediation to verify |

### Ready for QA (1 issue)

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

Consider transitioning TC-9020 to **ON_QA**.
