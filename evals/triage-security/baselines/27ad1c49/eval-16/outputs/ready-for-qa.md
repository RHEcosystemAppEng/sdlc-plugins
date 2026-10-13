# Ready for QA — Filtering Analysis

## Overview

Query 3 searches for triaged CVE Vulnerability issues that are not yet Closed, Verified, or ON_QA. For each candidate, the linked remediation Tasks (link type "Depend") are inspected. An issue qualifies as Ready for QA only when ALL linked remediation Tasks are in a terminal status (Done or Closed) and at least one such link exists.

**JQL**: `project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC`

3 candidates returned.

---

## TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

**Status**: Modified
**Created**: 2026-05-15

### Linked Remediation Tasks (Depend)

| Linked Task | Type | Status |
|-------------|------|--------|
| TC-9021 | Task | Done |
| TC-9022 | Task | Closed |

### Analysis

- 2 remediation Tasks linked via "Depend" relationship.
- TC-9021 status is **Done** -- terminal, qualifies.
- TC-9022 status is **Closed** -- terminal, qualifies.
- ALL linked remediation Tasks are in a completed state.

### Result: QUALIFIED -- Ready for QA

All linked remediation Tasks are completed (Done or Closed). This issue is a candidate for ON_QA transition.

---

## TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

**Status**: In Progress
**Created**: 2026-05-10

### Linked Remediation Tasks (Depend)

| Linked Task | Type | Status |
|-------------|------|--------|
| TC-9024 | Task | Done |
| TC-9025 | Task | In Progress |

### Analysis

- 2 remediation Tasks linked via "Depend" relationship.
- TC-9024 status is **Done** -- terminal, qualifies.
- TC-9025 status is **In Progress** -- NOT terminal, does not qualify.
- At least one linked Task is still open.

### Result: EXCLUDED -- Remediation in progress

TC-9025 is still In Progress. The issue cannot move to ON_QA until all remediation Tasks are completed.

---

## TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

**Status**: Modified
**Created**: 2026-05-05

### Linked Remediation Tasks (Depend)

No linked issues with link type "Depend" found.

### Analysis

- 0 remediation Tasks linked via "Depend" relationship.
- Without linked remediation Tasks, there is no remediation work to verify.

### Result: EXCLUDED -- No remediation to verify

No Depend links exist on this issue. An issue with no linked remediation Tasks cannot be verified as Ready for QA because there is no completed remediation to confirm.

---

## Summary

| Issue | CVE | Status | Depend Links | All Tasks Done? | Ready for QA? |
|-------|-----|--------|--------------|-----------------|---------------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | No |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A | No |

**1 of 3 candidates qualified for Ready for QA**: TC-9020 (CVE-2026-38901).
