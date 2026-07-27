# Ready for QA — Filtering Analysis

## Overview

Query 3 searches for triaged Vulnerability issues that are candidates for ON_QA transition. The JQL selects issues with the `ai-cve-triaged` label whose status is not already Closed, Verified, or ON_QA:

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

This query returned 3 candidate issues. Each candidate is then filtered by inspecting its `issuelinks` for linked Tasks with link type "Depend". The filtering rules are:

1. **ALL linked remediation Tasks are Done or Closed** — include in Ready for QA list.
2. **ANY linked Task is still open** — exclude. Remediation is still in progress.
3. **NO linked Tasks with type "Depend" exist** — exclude. No remediation to verify.

---

## Candidate Analysis

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status**: Modified
- **Created**: 2026-05-15
- **Depend links**: TC-9021 (Task, Done), TC-9022 (Task, Closed)
- **Analysis**: Both linked remediation Tasks are in terminal states (Done and Closed). All remediation work is complete.
- **Result**: **QUALIFIED** — Ready for QA. Consider transitioning to ON_QA.

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status**: In Progress
- **Created**: 2026-05-10
- **Depend links**: TC-9024 (Task, Done), TC-9025 (Task, In Progress)
- **Analysis**: TC-9024 is Done, but TC-9025 is still In Progress. Not all linked remediation Tasks are in a completed state.
- **Result**: **EXCLUDED** — Remediation in progress (TC-9025 is In Progress).

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status**: Modified
- **Created**: 2026-05-05
- **Depend links**: None (no Depend links found)
- **Analysis**: This issue has no linked Tasks with link type "Depend". Without remediation tasks, there is nothing to verify in QA.
- **Result**: **EXCLUDED** — No remediation tasks to verify.

---

## Summary

| Issue | CVE | Depend Links | All Tasks Completed? | Ready for QA? |
|-------|-----|--------------|---------------------|---------------|
| TC-9020 | CVE-2026-38901 | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes |
| TC-9023 | CVE-2026-39102 | TC-9024 (Done), TC-9025 (In Progress) | No | No — open task |
| TC-9026 | CVE-2026-39330 | (none) | N/A | No — no Depend links |

**1 of 3 candidates qualified for Ready for QA: TC-9020.**
