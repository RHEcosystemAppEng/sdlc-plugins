# Ready for QA Filtering Analysis

## Overview

Query 3 searches for triaged CVE issues that are not yet in a terminal or QA state:

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

This query returned 3 candidate issues. Each candidate is evaluated by inspecting its `issuelinks` for linked Tasks with link type "Depend". The filtering rules are:

1. **ALL linked remediation Tasks are Done or Closed** -- include in Ready for QA list.
2. **ANY linked Task is still open** -- exclude (remediation still in progress).
3. **NO linked Tasks with type "Depend" exist** -- exclude (no remediation to verify).

---

## Candidate Analysis

### TC-9020 -- CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status**: Modified
- **CVE**: CVE-2026-38901
- **Created**: 2026-05-15

**Linked Remediation Tasks (Depend type):**

| Task Key | Issue Type | Status | Completed? |
|----------|-----------|--------|------------|
| TC-9021 | Task | Done | Yes |
| TC-9022 | Task | Closed | Yes |

**Evaluation**: ALL linked remediation Tasks are in a completed state (Done or Closed). Both TC-9021 and TC-9022 have finished their work.

**Result**: **INCLUDED** in Ready for QA list.

**Recommended Action**: Consider transitioning TC-9020 to ON_QA. All remediation work has been completed and the vulnerability fix is ready for quality assurance verification.

---

### TC-9023 -- CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status**: In Progress
- **CVE**: CVE-2026-39102
- **Created**: 2026-05-10

**Linked Remediation Tasks (Depend type):**

| Task Key | Issue Type | Status | Completed? |
|----------|-----------|--------|------------|
| TC-9024 | Task | Done | Yes |
| TC-9025 | Task | In Progress | No |

**Evaluation**: TC-9025 is still In Progress. The rule requires ALL linked Tasks to be Done or Closed. Since TC-9025 has not yet completed, this issue fails the readiness check.

**Result**: **EXCLUDED** -- remediation is still in progress (TC-9025 In Progress).

**Recommended Action**: No action until TC-9025 is completed. Monitor TC-9025 for completion before re-evaluating.

---

### TC-9026 -- CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status**: Modified
- **CVE**: CVE-2026-39330
- **Created**: 2026-05-05

**Linked Remediation Tasks (Depend type):**

None. This issue has no linked Tasks with link type "Depend".

**Evaluation**: The filtering rule requires at least one linked Depend-type Task to exist. Without any remediation tasks linked, there is nothing to verify as complete. This could indicate that remediation tasks were not yet created, were linked with a different link type, or that the issue was resolved through other means not tracked via Depend links.

**Result**: **EXCLUDED** -- no linked Tasks with type "Depend" found. No remediation to verify.

**Recommended Action**: Investigate why TC-9026 has no Depend-linked remediation tasks. If remediation was completed outside of Jira task tracking, manual verification may be needed before transitioning to QA.

---

## Summary Table

| Issue | CVE | Status | Depend-linked Tasks | All Tasks Complete? | Ready for QA? |
|-------|-----|--------|---------------------|---------------------|---------------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | No |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A | No |

## Qualified Issues

Only **TC-9020** qualifies for Ready for QA. Suggested action: transition TC-9020 to ON_QA.
