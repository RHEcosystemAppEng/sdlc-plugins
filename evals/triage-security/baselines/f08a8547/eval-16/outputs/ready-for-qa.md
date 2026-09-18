# Ready for QA — Filtering Analysis

**Date**: 2026-09-08
**Project**: TC

## Overview

Query 3 searches for triaged Vulnerability issues that are not yet in a terminal or QA state, to identify CVEs whose remediation work is complete and ready for QA verification.

**JQL**: `project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC`

**Candidates returned**: 3 issues

## Filtering Criteria

For each candidate, the filtering logic inspects `issuelinks` for linked Tasks with link type "Depend":

1. **ALL linked remediation Tasks are Done or Closed** -- include in Ready for QA list
2. **ANY linked Task is still open** -- exclude (remediation still in progress)
3. **NO linked Tasks with type "Depend" exist** -- exclude (no remediation to verify)

---

## Candidate Analysis

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status**: Modified
- **CVE**: CVE-2026-38901
- **Created**: 2026-05-15

**Linked remediation tasks (Depend)**:

| Linked Task | Type | Status | Completed? |
|-------------|------|--------|------------|
| TC-9021 | Task | Done | Yes |
| TC-9022 | Task | Closed | Yes |

**Result**: **QUALIFIED — Ready for QA**

All linked remediation Tasks are in a completed state (Done or Closed). This CVE has finished remediation and is a candidate for ON_QA transition.

---

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status**: In Progress
- **CVE**: CVE-2026-39102
- **Created**: 2026-05-10

**Linked remediation tasks (Depend)**:

| Linked Task | Type | Status | Completed? |
|-------------|------|--------|------------|
| TC-9024 | Task | Done | Yes |
| TC-9025 | Task | In Progress | No |

**Result**: **EXCLUDED — Remediation in progress**

TC-9025 is still In Progress. Not all linked remediation Tasks are complete, so this CVE cannot move to QA yet. Once TC-9025 reaches Done or Closed status, this issue will qualify.

---

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status**: Modified
- **CVE**: CVE-2026-39330
- **Created**: 2026-05-05

**Linked remediation tasks (Depend)**: None

**Result**: **EXCLUDED — No remediation to verify**

This issue has no linked Tasks with link type "Depend". Without remediation tasks, there is nothing to verify in QA. This may indicate that remediation tasks have not yet been created, or the issue was resolved through a different mechanism.

---

## Summary

| Issue | CVE | Status | Depend Links | All Tasks Done? | Ready for QA? |
|-------|-----|--------|--------------|-----------------|---------------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | No |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A | No |

**Total candidates**: 3
**Qualified for QA**: 1 (TC-9020)
**Excluded**: 2 (TC-9023 — open task; TC-9026 — no Depend links)
