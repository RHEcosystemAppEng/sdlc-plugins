# Ready for QA — Detailed Filtering Analysis

## Query 3 JQL

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

This query uses:
- **Project key** `TC` from Jira Configuration
- **Vulnerability issue type ID** `10024` from Security Configuration
- `labels IN (ai-cve-triaged)` to find triaged CVEs
- `status NOT IN (Closed, Verified, 'ON_QA')` to find CVEs still in a pre-QA state

The query returned 3 issues. For each, the skill checks `issuelinks` for linked Tasks with link type `Depend` and fetches each linked Task's status to determine if all remediation is complete.

---

## Issue-by-Issue Filtering

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

**Status**: Modified
**Created**: 2026-05-15
**Labels**: CVE-2026-38901, pscomponent:org/rhtpa-server, ai-cve-triaged

**Linked Remediation Tasks (Depend)**:

| Task | Type | Status | Complete? |
|------|------|--------|-----------|
| TC-9021 | Task | Done | Yes |
| TC-9022 | Task | Closed | Yes |

**Assessment**: ALL linked remediation Tasks are completed (TC-9021 is Done, TC-9022 is Closed).

**Result**: **INCLUDED in Ready for QA**

**Recommendation**: Consider transitioning TC-9020 to ON_QA. All remediation tasks have been completed — the fix is ready for QA verification.

---

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

**Status**: In Progress
**Created**: 2026-05-10
**Labels**: CVE-2026-39102, pscomponent:org/rhtpa-server, ai-cve-triaged

**Linked Remediation Tasks (Depend)**:

| Task | Type | Status | Complete? |
|------|------|--------|-----------|
| TC-9024 | Task | Done | Yes |
| TC-9025 | Task | In Progress | **No** |

**Assessment**: TC-9025 is still In Progress — remediation is not yet complete. Not all linked Tasks are in a terminal state (Done or Closed).

**Result**: **EXCLUDED from Ready for QA** — remediation still in progress.

---

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

**Status**: Modified
**Created**: 2026-05-05
**Labels**: CVE-2026-39330, pscomponent:org/rhtpa-server, ai-cve-triaged

**Linked Remediation Tasks (Depend)**: None

**Assessment**: No linked Tasks with type `Depend` exist on this issue. Without linked remediation tasks, there is no remediation work to verify completion of.

**Result**: **EXCLUDED from Ready for QA** — no remediation tasks linked to verify.

---

## Summary

| Issue | CVE | Remediation Tasks | All Complete? | Ready for QA? |
|-------|-----|-------------------|---------------|---------------|
| TC-9020 | CVE-2026-38901 | TC-9021 (Done), TC-9022 (Closed) | Yes | **Yes** |
| TC-9023 | CVE-2026-39102 | TC-9024 (Done), TC-9025 (In Progress) | No | No |
| TC-9026 | CVE-2026-39330 | (none) | N/A | No |

**1 of 3** Query 3 candidates qualifies for Ready for QA transition.
