# Ready for QA — Filtering Analysis

## Query

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

This query returns triaged Vulnerability issues that are not yet Closed, Verified, or ON_QA — candidates whose remediation may be complete and ready for QA verification.

## Candidates (3 issues returned)

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status**: Modified
- **Labels**: CVE-2026-38901, pscomponent:org/rhtpa-server, ai-cve-triaged
- **Created**: 2026-05-15
- **Linked Tasks (Depend)**:
  - TC-9021 (Task) — **Done**
  - TC-9022 (Task) — **Closed**
- **Assessment**: ALL linked remediation Tasks are in a terminal state (Done or Closed).
- **Result**: **QUALIFIED — Ready for QA**
- **Recommendation**: Consider transitioning TC-9020 to ON_QA.

---

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status**: In Progress
- **Labels**: CVE-2026-39102, pscomponent:org/rhtpa-server, ai-cve-triaged
- **Created**: 2026-05-10
- **Linked Tasks (Depend)**:
  - TC-9024 (Task) — **Done**
  - TC-9025 (Task) — **In Progress**
- **Assessment**: TC-9025 is still In Progress. Not all linked remediation Tasks are complete.
- **Result**: **EXCLUDED — Remediation in progress**
- **Reason**: At least one linked remediation Task (TC-9025) has not reached a terminal state. The CVE cannot move to QA until all remediation work is done.

---

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status**: Modified
- **Labels**: CVE-2026-39330, pscomponent:org/rhtpa-server, ai-cve-triaged
- **Created**: 2026-05-05
- **Linked Tasks (Depend)**: (none)
- **Assessment**: No linked Tasks with link type "Depend" exist on this issue.
- **Result**: **EXCLUDED — No remediation to verify**
- **Reason**: Without linked remediation Tasks, there is no completed work to verify in QA. This issue may need remediation tasks created before it can progress.

## Summary

| Issue | CVE | Status | Linked Tasks | All Tasks Complete? | Ready for QA? |
|-------|-----|--------|--------------|---------------------|---------------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | No |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A | No |

**1 of 3 candidates qualified for Ready for QA transition.**

### Filtering Rules Applied

1. **ALL linked remediation Tasks must be Done or Closed** — TC-9020 met this criterion (TC-9021 Done, TC-9022 Closed).
2. **ANY linked Task still open excludes the issue** — TC-9023 was excluded because TC-9025 is In Progress.
3. **NO linked Tasks with type "Depend" excludes the issue** — TC-9026 was excluded because it has no Depend links, meaning there is no remediation work to verify.
