# Ready for QA — Filtering Analysis

## Query

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

This query returns triaged Vulnerability issues that are not yet in a terminal or QA state. Each candidate is then filtered by inspecting its `issuelinks` for linked Tasks with link type "Depend".

## Candidates Evaluated (3 issues)

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status**: Modified
- **Labels**: CVE-2026-38901, pscomponent:org/rhtpa-server, ai-cve-triaged
- **Created**: 2026-05-15
- **Depend links**:
  - TC-9021 (Task) — **Done**
  - TC-9022 (Task) — **Closed**
- **Analysis**: Both linked remediation Tasks have completed statuses (Done and Closed). All Depend-linked Tasks are finished.
- **Result**: **QUALIFIED — Ready for QA**
- **Recommendation**: Consider transitioning TC-9020 to ON_QA.

---

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status**: In Progress
- **Labels**: CVE-2026-39102, pscomponent:org/rhtpa-server, ai-cve-triaged
- **Created**: 2026-05-10
- **Depend links**:
  - TC-9024 (Task) — **Done**
  - TC-9025 (Task) — **In Progress**
- **Analysis**: TC-9025 is still In Progress. Not all linked remediation Tasks are completed.
- **Result**: **EXCLUDED — remediation in progress**
- **Reason**: TC-9025 (Task) remains In Progress. Until all Depend-linked Tasks reach Done or Closed status, this CVE cannot move to QA.

---

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status**: Modified
- **Labels**: CVE-2026-39330, pscomponent:org/rhtpa-server, ai-cve-triaged
- **Created**: 2026-05-05
- **Depend links**: (none)
- **Analysis**: No linked Tasks with link type "Depend" exist on this issue.
- **Result**: **EXCLUDED — no remediation to verify**
- **Reason**: Without Depend-linked remediation Tasks, there is no completed remediation work to verify in QA. This issue may still need remediation task creation or may have been closed/resolved through another path.

---

## Summary

| Issue | CVE | Status | Depend Links | All Tasks Done? | Ready for QA? |
|-------|-----|--------|-------------|-----------------|---------------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | No |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A | No |

**Qualified for QA: 1 of 3 candidates (TC-9020)**

### Filtering Rules Applied

Per the triage-security skill discovery mode (Query 3):

1. **ALL linked remediation Tasks are Done or Closed** -- include in Ready for QA list (TC-9020 qualified)
2. **ANY linked Task is still open** -- exclude, remediation is still in progress (TC-9023 excluded)
3. **NO linked Tasks with type "Depend" exist** -- exclude, no remediation to verify (TC-9026 excluded)
