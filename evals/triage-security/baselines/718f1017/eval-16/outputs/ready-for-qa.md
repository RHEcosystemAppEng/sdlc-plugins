# Ready for QA — Detailed Filtering Analysis

## Overview

This analysis evaluates the Query 3 results (triaged CVEs that are not yet Closed, Verified, or ON_QA) to determine which issues qualify as "Ready for QA" -- meaning all linked remediation Tasks are completed and the CVE is a candidate for ON_QA transition.

## Methodology

Per the triage-security skill (SKILL.md, Discovery Mode, Query 3):

1. Search for triaged Vulnerability issues not yet closed or in QA:
   ```
   project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
   ```

2. For each result, inspect its `issuelinks` for linked Tasks with link type "Depend".

3. Apply the following filtering rules:
   - **ALL linked remediation Tasks are Done or Closed** --> include in "Ready for QA" list. These CVEs have completed remediation and are candidates for ON_QA transition.
   - **ANY linked Task is still open** --> exclude. Remediation is still in progress.
   - **NO linked Tasks with type "Depend" exist** --> exclude. No remediation to verify.

## Candidate Issues (3 total)

### TC-9020 -- CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status**: Modified
- **CVE**: CVE-2026-38901
- **Created**: 2026-05-15
- **Labels**: CVE-2026-38901, pscomponent:org/rhtpa-server, ai-cve-triaged

**Linked Remediation Tasks (link type "Depend"):**

| Task Key | Issue Type | Status |
|----------|-----------|--------|
| TC-9021 | Task | Done |
| TC-9022 | Task | Closed |

**Analysis**: Both linked remediation Tasks have completed statuses:
- TC-9021: **Done** (completed status)
- TC-9022: **Closed** (completed status)

ALL linked remediation Tasks are Done or Closed.

**Result: QUALIFIED -- Ready for QA**

Recommendation: Consider transitioning TC-9020 to ON_QA.

---

### TC-9023 -- CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status**: In Progress
- **CVE**: CVE-2026-39102
- **Created**: 2026-05-10
- **Labels**: CVE-2026-39102, pscomponent:org/rhtpa-server, ai-cve-triaged

**Linked Remediation Tasks (link type "Depend"):**

| Task Key | Issue Type | Status |
|----------|-----------|--------|
| TC-9024 | Task | Done |
| TC-9025 | Task | In Progress |

**Analysis**: Not all linked remediation Tasks are completed:
- TC-9024: **Done** (completed status)
- TC-9025: **In Progress** (still open -- remediation in progress)

ANY linked Task is still open, so this issue is excluded. TC-9025 must reach Done or Closed status before TC-9023 can be considered Ready for QA.

**Result: EXCLUDED -- Remediation still in progress**

Reason: TC-9025 is still In Progress. The rule requires ALL linked remediation Tasks to be Done or Closed. Since TC-9025 is not yet complete, remediation is still in progress.

---

### TC-9026 -- CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status**: Modified
- **CVE**: CVE-2026-39330
- **Created**: 2026-05-05
- **Labels**: CVE-2026-39330, pscomponent:org/rhtpa-server, ai-cve-triaged

**Linked Remediation Tasks (link type "Depend"):**

(none)

**Analysis**: This issue has no linked Tasks with link type "Depend". Without remediation tasks to verify, this issue cannot be considered Ready for QA. It may need remediation tasks created first, or it may have been triaged and closed as not affected (but remains open, which is unusual).

**Result: EXCLUDED -- No remediation to verify**

Reason: No linked Tasks with type "Depend" exist. The rule states that issues with no Depend links are excluded because there is no remediation to verify.

---

## Summary

| Issue | CVE | Status | Depend Links | All Tasks Complete? | Ready for QA? |
|-------|-----|--------|--------------|---------------------|---------------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No (TC-9025 open) | No |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A (no tasks) | No |

**Final Ready for QA list: 1 issue**
- **TC-9020** (CVE-2026-38901): All remediation tasks completed. Recommend transitioning to ON_QA.

**Excluded: 2 issues**
- **TC-9023**: Excluded because TC-9025 is still In Progress (ANY linked Task is still open).
- **TC-9026**: Excluded because no linked Tasks with type "Depend" exist (no remediation to verify).
