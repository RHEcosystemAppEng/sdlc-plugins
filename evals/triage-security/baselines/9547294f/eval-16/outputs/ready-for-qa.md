# Ready for QA — Detailed Filtering Analysis

## Overview

The third JQL query identifies triaged CVE issues that are in a pre-QA state — they have been triaged (`ai-cve-triaged` label present) but have not yet reached ON_QA, Verified, or Closed status. These are candidates for transitioning to ON_QA once all linked remediation tasks are completed.

## JQL Query

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

This query uses:
- **Project key**: `TC` (from Jira Configuration)
- **Vulnerability issue type ID**: `10024` (from Security Configuration)
- **Label filter**: `ai-cve-triaged` — ensures only previously triaged issues are considered
- **Status exclusion**: `Closed, Verified, ON_QA` — excludes issues already in terminal or QA states

## Query Results (3 issues)

The query returned 3 issues. For each, the skill inspects `issuelinks` for linked Tasks with link type "Depend" and fetches each linked Task's status.

---

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

**Status**: Modified
**Created**: 2026-05-15
**Labels**: CVE-2026-38901, pscomponent:org/rhtpa-server, ai-cve-triaged

**Linked Remediation Tasks (Depend type)**:

| Task Key | Issue Type | Status | Completed? |
|----------|-----------|--------|------------|
| TC-9021 | Task | Done | Yes |
| TC-9022 | Task | Closed | Yes |

**Filtering Decision**: **INCLUDED in Ready for QA**

**Reason**: ALL linked remediation Tasks are in a completed state (Done or Closed). Both TC-9021 (Done) and TC-9022 (Closed) have finished. Remediation is fully complete for this CVE.

**Recommendation**: Consider transitioning TC-9020 to ON_QA. All remediation work has been completed and the fix is ready for quality assurance verification.

---

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

**Status**: In Progress
**Created**: 2026-05-10
**Labels**: CVE-2026-39102, pscomponent:org/rhtpa-server, ai-cve-triaged

**Linked Remediation Tasks (Depend type)**:

| Task Key | Issue Type | Status | Completed? |
|----------|-----------|--------|------------|
| TC-9024 | Task | Done | Yes |
| TC-9025 | Task | In Progress | No |

**Filtering Decision**: **EXCLUDED from Ready for QA**

**Reason**: TC-9025 is still In Progress — remediation is not complete. Even though TC-9024 is Done, ALL linked remediation Tasks must be in a completed state (Done or Closed) for the CVE to qualify as Ready for QA. The incomplete task TC-9025 blocks the transition.

---

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

**Status**: Modified
**Created**: 2026-05-05
**Labels**: CVE-2026-39330, pscomponent:org/rhtpa-server, ai-cve-triaged

**Linked Remediation Tasks (Depend type)**:

| Task Key | Issue Type | Status | Completed? |
|----------|-----------|--------|------------|
| (none) | — | — | — |

**Filtering Decision**: **EXCLUDED from Ready for QA**

**Reason**: No linked Tasks with type "Depend" exist on this issue. Without remediation tasks to verify, there is no evidence that a fix has been implemented. Issues with no Depend links cannot be considered Ready for QA — there is no remediation to verify.

---

## Summary

| Issue | Linked Tasks | All Completed? | Ready for QA? | Reason |
|-------|-------------|----------------|---------------|--------|
| TC-9020 | TC-9021 (Done), TC-9022 (Closed) | Yes | **Yes** | All remediation tasks completed |
| TC-9023 | TC-9024 (Done), TC-9025 (In Progress) | No | **No** | TC-9025 still In Progress |
| TC-9026 | (none) | N/A | **No** | No Depend links — no remediation to verify |

## Ready for QA Table

Only TC-9020 qualifies for the Ready for QA list:

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

> Consider transitioning TC-9020 to ON_QA.
