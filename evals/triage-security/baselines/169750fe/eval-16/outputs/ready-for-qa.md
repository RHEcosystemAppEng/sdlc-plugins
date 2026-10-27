# Ready for QA — Filtering Analysis

## Query

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

This query returns triaged Vulnerability issues that are not yet closed, verified, or in QA. Each result is then checked for linked remediation Tasks (link type "Depend") to determine whether all remediation work is complete.

## Candidates Evaluated

3 issues returned by the query.

---

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status**: Modified
- **Created**: 2026-05-15
- **Issue Links (Depend type)**:
  - TC-9021 (Task) — **Done**
  - TC-9022 (Task) — **Closed**
- **Analysis**: All linked remediation Tasks have completed statuses (Done or Closed). Both TC-9021 and TC-9022 are finished.
- **Result**: **INCLUDED** — Ready for QA
- **Recommendation**: Consider transitioning TC-9020 to ON_QA.

---

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status**: In Progress
- **Created**: 2026-05-10
- **Issue Links (Depend type)**:
  - TC-9024 (Task) — **Done**
  - TC-9025 (Task) — **In Progress**
- **Analysis**: TC-9025 is still In Progress. Not all linked remediation Tasks are complete.
- **Result**: **EXCLUDED** — Remediation still in progress

---

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status**: Modified
- **Created**: 2026-05-05
- **Issue Links (Depend type)**: None
- **Analysis**: No linked Tasks with link type "Depend" exist. There is no remediation work to verify completion against.
- **Result**: **EXCLUDED** — No linked remediation Tasks

---

## Summary

| Issue | CVE | Linked Tasks | All Complete? | Ready for QA? |
|-------|-----|-------------|---------------|---------------|
| TC-9020 | CVE-2026-38901 | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes |
| TC-9023 | CVE-2026-39102 | TC-9024 (Done), TC-9025 (In Progress) | No | No |
| TC-9026 | CVE-2026-39330 | (none) | N/A | No |

**1 issue qualifies for Ready for QA: TC-9020**

### Filtering Rules Applied

1. For each Query 3 result, inspect `issuelinks` for entries where `type.name` is "Depend".
2. For each linked Task, fetch its current status.
3. **Include** only if ALL linked remediation Tasks have a terminal status (Done or Closed).
4. **Exclude** if ANY linked Task is still open (not Done/Closed).
5. **Exclude** if NO linked Tasks with type "Depend" exist — no remediation to verify.
