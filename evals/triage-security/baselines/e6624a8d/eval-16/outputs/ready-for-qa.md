# Ready for QA — Filtering Analysis

## Overview

Query 3 searched for triaged Vulnerability issues (label `ai-cve-triaged`) that are not yet in a terminal or QA state:

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

This returned 3 candidate issues. Each was evaluated by inspecting its `issuelinks` for linked Tasks with link type "Depend" to determine whether all remediation work is complete.

## Filtering Criteria

An issue qualifies as "Ready for QA" only when:
1. It has at least one linked Task with link type "Depend".
2. ALL such linked Tasks are in a completed status (Done or Closed).

An issue is excluded if:
- Any linked "Depend" Task is still open (remediation in progress).
- No linked Tasks with type "Depend" exist (no remediation to verify).

## Candidate Analysis

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status**: Modified
- **Linked remediation Tasks**:
  - TC-9021 (Task) — **Done**
  - TC-9022 (Task) — **Closed**
- **Evaluation**: All 2 linked remediation Tasks are in a completed status (Done or Closed).
- **Result**: **QUALIFIED — Ready for QA**
- **Recommendation**: Consider transitioning TC-9020 to ON_QA.

---

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status**: In Progress
- **Linked remediation Tasks**:
  - TC-9024 (Task) — **Done**
  - TC-9025 (Task) — **In Progress**
- **Evaluation**: TC-9025 is still In Progress. Not all remediation Tasks are complete.
- **Result**: **EXCLUDED — Remediation in progress**
- **Reason**: 1 of 2 linked Tasks (TC-9025) is still open. Remediation must complete before this issue can move to QA.

---

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status**: Modified
- **Linked remediation Tasks**: (none with link type "Depend")
- **Evaluation**: No linked Tasks with type "Depend" found.
- **Result**: **EXCLUDED — No remediation to verify**
- **Reason**: Without linked remediation Tasks, there is no completed work to verify in QA. This issue may need remediation tasks created first.

## Summary

| Issue | CVE | Status | Linked Tasks | All Complete? | Ready for QA? |
|-------|-----|--------|--------------|---------------|---------------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | No — open task |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A | No — no Depend links |

**Result**: 1 of 3 candidates qualified for QA transition.
