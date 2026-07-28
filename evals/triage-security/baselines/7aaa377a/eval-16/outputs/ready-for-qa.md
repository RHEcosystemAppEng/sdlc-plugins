# Ready for QA — Detailed Filtering Analysis

## Overview

The Ready for QA query identifies triaged CVE Vulnerability issues whose remediation
work is complete and are candidates for transition to ON_QA status.

## JQL Query

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

This query uses:
- Project key **TC** (from Jira Configuration)
- Vulnerability issue type ID **10024** (from Security Configuration)
- Label filter `ai-cve-triaged` to select only previously triaged issues
- Status exclusion `NOT IN (Closed, Verified, 'ON_QA')` to find issues still in a pre-QA state

The query returned **3 issues**. Each is evaluated below by inspecting its
`issuelinks` for linked Tasks with link type "Depend" and checking each linked
Task's status.

---

## Issue-by-Issue Filtering

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status**: Modified
- **CVE**: CVE-2026-38901
- **Created**: 2026-05-15

**Linked remediation Tasks (Depend link type):**

| Task Key | Issue Type | Status | Completed? |
|----------|-----------|--------|------------|
| TC-9021 | Task | Done | Yes |
| TC-9022 | Task | Closed | Yes |

**Evaluation**: ALL linked remediation Tasks are in a completed state (Done or Closed).

**Result**: **INCLUDED** in Ready for QA.

**Recommendation**: Consider transitioning TC-9020 to ON_QA. All remediation work
has been completed — TC-9021 is Done and TC-9022 is Closed.

---

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status**: In Progress
- **CVE**: CVE-2026-39102
- **Created**: 2026-05-10

**Linked remediation Tasks (Depend link type):**

| Task Key | Issue Type | Status | Completed? |
|----------|-----------|--------|------------|
| TC-9024 | Task | Done | Yes |
| TC-9025 | Task | In Progress | No |

**Evaluation**: NOT all linked remediation Tasks are completed. TC-9025 is still
In Progress — remediation is not yet complete.

**Result**: **EXCLUDED** from Ready for QA.

**Reason**: TC-9025 is still In Progress. The CVE cannot move to ON_QA until all
linked remediation Tasks are Done or Closed. Once TC-9025 completes, TC-9023 will
qualify.

---

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status**: Modified
- **CVE**: CVE-2026-39330
- **Created**: 2026-05-05

**Linked remediation Tasks (Depend link type):**

No linked Tasks with link type "Depend" were found on this issue.

**Evaluation**: The issue has no Depend links to remediation Tasks. Without linked
remediation Tasks, there is no remediation work to verify.

**Result**: **EXCLUDED** from Ready for QA.

**Reason**: No linked Tasks with type Depend exist on this issue. There is no
remediation to verify. This issue may need investigation — a triaged CVE should
normally have remediation tasks linked via Depend, unless it was closed as
Not a Bug (but this issue is in Modified status, not Closed).

---

## Filtering Summary

| Issue | CVE | Status | Depend Links | All Tasks Complete? | Ready for QA? |
|-------|-----|--------|-------------|---------------------|---------------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | No |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A | No |

## Filtering Rules Applied

The filtering logic follows SKILL.md discovery mode, Query 3:

1. For each issue returned by the Ready for QA JQL query, check its `issuelinks`
   for linked Tasks with link type "Depend".
2. For each linked Task (extracted from `outwardIssue.key` or `inwardIssue.key`),
   fetch the Task's status.
3. **ALL linked remediation Tasks are Done or Closed** — include in the Ready for QA
   list. These CVEs have completed remediation and are candidates for ON_QA transition.
4. **ANY linked Task is still open** (not Done or Closed) — exclude. Remediation
   is still in progress.
5. **NO linked Tasks with type "Depend" exist** — exclude. No remediation to verify.

## Recommended Actions

- **TC-9020**: Transition to ON_QA. All remediation Tasks (TC-9021, TC-9022) are
  completed.
