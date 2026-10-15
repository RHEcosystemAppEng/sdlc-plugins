# Ready for QA — Detailed Filtering Analysis

## Query Construction

The Ready for QA query is the third JQL query in discovery mode, constructed from the Security Configuration:

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

- `project = TC` — project key from Jira Configuration
- `issuetype = 10024` — vulnerability issue type ID from Security Configuration
- `labels IN (ai-cve-triaged)` — only triaged CVEs (marked by prior triage runs)
- `status NOT IN (Closed, Verified, 'ON_QA')` — excludes issues already closed, verified, or in QA — finds triaged CVEs still in a pre-QA state

This query returned 3 issues: TC-9020, TC-9023, and TC-9026.

## Filtering Procedure

For each query 3 result, the skill checks the issue's `issuelinks` for linked Tasks with link type `Depend` and fetches each linked Task's status:

1. If **ALL** linked remediation Tasks (Depend link type) have status Done or Closed, the issue qualifies as **Ready for QA**.
2. If **ANY** linked Task is still open (not Done or Closed), the issue is **excluded** — remediation is not yet complete.
3. If the issue has **NO** linked Tasks with type Depend, the issue is **excluded** — there is no remediation to verify.

---

## Issue-by-Issue Analysis

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status**: Modified
- **CVE**: CVE-2026-38901
- **Labels**: CVE-2026-38901, pscomponent:org/rhtpa-server, ai-cve-triaged
- **Created**: 2026-05-15

**Linked remediation Tasks (Depend link type):**

| Task | Type | Status | Completed? |
|------|------|--------|------------|
| TC-9021 | Task | Done | Yes |
| TC-9022 | Task | Closed | Yes |

**Assessment**: ALL linked remediation Tasks are completed (TC-9021 Done, TC-9022 Closed).

**Result**: **INCLUDED in Ready for QA**

**Recommendation**: Consider transitioning TC-9020 to **ON_QA**. All remediation work is complete and the fixes are ready for QA verification.

---

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status**: In Progress
- **CVE**: CVE-2026-39102
- **Labels**: CVE-2026-39102, pscomponent:org/rhtpa-server, ai-cve-triaged
- **Created**: 2026-05-10

**Linked remediation Tasks (Depend link type):**

| Task | Type | Status | Completed? |
|------|------|--------|------------|
| TC-9024 | Task | Done | Yes |
| TC-9025 | Task | In Progress | No |

**Assessment**: TC-9025 is still **In Progress** — not all remediation Tasks are complete. Remediation work is ongoing.

**Result**: **EXCLUDED from Ready for QA** — remediation is not complete (TC-9025 In Progress)

---

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status**: Modified
- **CVE**: CVE-2026-39330
- **Labels**: CVE-2026-39330, pscomponent:org/rhtpa-server, ai-cve-triaged
- **Created**: 2026-05-05

**Linked remediation Tasks (Depend link type):**

No `issuelinks` entries with link type `Depend` were found on this issue.

**Assessment**: There are no linked remediation Tasks with type Depend. Without linked remediation tasks, there is nothing to verify as complete.

**Result**: **EXCLUDED from Ready for QA** — no linked Tasks with type Depend (no remediation to verify)

---

## Summary

| Issue | CVE | Status | Remediation Tasks | Ready for QA? | Reason |
|-------|-----|--------|-------------------|---------------|--------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | All remediation Tasks completed |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | TC-9025 still In Progress |
| TC-9026 | CVE-2026-39330 | Modified | (none) | No | No Depend links — no remediation to verify |

**Action items:**
- **TC-9020**: Propose transitioning to **ON_QA** — all linked remediation Tasks are Done/Closed and the fixes are ready for quality assurance verification.
