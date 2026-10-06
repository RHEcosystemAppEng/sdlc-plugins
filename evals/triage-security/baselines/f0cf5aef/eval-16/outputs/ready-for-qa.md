# Ready for QA — Filtering Analysis

## Overview

Query 3 searched for triaged Vulnerability issues (`ai-cve-triaged` label) that are not yet Closed, Verified, or ON_QA. For each candidate, the filtering checks whether all linked remediation Tasks (link type "Depend") are completed (Done or Closed).

**JQL**: `project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC`

**Candidates returned**: 3

---

## Candidate Analysis

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status**: Modified
- **Created**: 2026-05-15
- **Linked remediation Tasks (Depend)**:
  - TC-9021 (Task) — **Done**
  - TC-9022 (Task) — **Closed**
- **Assessment**: ALL linked remediation Tasks are in a completed state (Done or Closed).
- **Result**: **QUALIFIED** — Ready for QA. Consider transitioning to ON_QA.

---

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status**: In Progress
- **Created**: 2026-05-10
- **Linked remediation Tasks (Depend)**:
  - TC-9024 (Task) — **Done**
  - TC-9025 (Task) — **In Progress**
- **Assessment**: TC-9025 is still In Progress. At least one linked remediation Task is not yet completed.
- **Result**: **EXCLUDED** — Remediation is still in progress.

---

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status**: Modified
- **Created**: 2026-05-05
- **Linked remediation Tasks (Depend)**: (none)
- **Assessment**: No linked Tasks with link type "Depend" found. Without remediation task links, there is nothing to verify as completed.
- **Result**: **EXCLUDED** — No remediation tasks to verify.

---

## Summary

| Issue | CVE | Status | Depend Links | All Tasks Done? | Ready for QA? |
|-------|-----|--------|--------------|-----------------|---------------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | No |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A | No |

**Qualified for ON_QA transition**: 1 issue (TC-9020)
**Excluded**: 2 issues (TC-9023 — open task; TC-9026 — no Depend links)
