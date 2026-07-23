# Ready for QA — Filtering Analysis

## Query

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged)
  AND status NOT IN (Closed, Verified, 'ON_QA')
  ORDER BY created DESC
```

This query returns triaged Vulnerability issues that are not yet Closed, Verified, or ON_QA. Each result is then evaluated against its linked remediation Tasks to determine readiness.

## Candidates Returned (3 issues)

| Issue | Status | CVE | Depend Links |
|-------|--------|-----|--------------|
| TC-9020 | Modified | CVE-2026-38901 | TC-9021 (Task, Done), TC-9022 (Task, Closed) |
| TC-9023 | In Progress | CVE-2026-39102 | TC-9024 (Task, Done), TC-9025 (Task, In Progress) |
| TC-9026 | Modified | CVE-2026-39330 | (none) |

## Filtering Criteria

Per the discovery mode protocol, a candidate qualifies as "Ready for QA" only when:

1. It has linked issues with link type "Depend" (remediation Tasks).
2. **All** such linked Tasks have a terminal status (Done or Closed).

Issues are excluded if:
- Any linked remediation Task is still open (not Done/Closed).
- No linked Tasks with type "Depend" exist (no remediation to verify).

## Per-Issue Analysis

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

**Status**: Modified
**Depend links**: 2 linked Tasks

| Linked Task | Type | Status | Terminal? |
|-------------|------|--------|-----------|
| TC-9021 | Task | Done | Yes |
| TC-9022 | Task | Closed | Yes |

**Result**: **QUALIFIED — Ready for QA**

All linked remediation Tasks are in a terminal status (Done or Closed). This CVE has completed remediation and is a candidate for ON_QA transition.

---

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

**Status**: In Progress
**Depend links**: 2 linked Tasks

| Linked Task | Type | Status | Terminal? |
|-------------|------|--------|-----------|
| TC-9024 | Task | Done | Yes |
| TC-9025 | Task | In Progress | No |

**Result**: **EXCLUDED — Remediation in progress**

TC-9025 is still In Progress. Not all linked remediation Tasks are complete. This CVE cannot move to ON_QA until TC-9025 reaches Done or Closed.

---

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

**Status**: Modified
**Depend links**: 0 linked Tasks

**Result**: **EXCLUDED — No remediation to verify**

This issue has no linked Tasks with link type "Depend". Without remediation Tasks, there is nothing to verify as complete. This may indicate that remediation tasks have not yet been created, or that the issue was triaged with a different outcome (e.g., close recommendation pending).

---

## Summary

| Issue | CVE | Qualified? | Reason |
|-------|-----|------------|--------|
| TC-9020 | CVE-2026-38901 | Yes | All 2 remediation Tasks complete (TC-9021 Done, TC-9022 Closed) |
| TC-9023 | CVE-2026-39102 | No | TC-9025 still In Progress (1 of 2 Tasks incomplete) |
| TC-9026 | CVE-2026-39330 | No | No Depend links (no remediation Tasks to verify) |

**1 of 3 candidates qualified for QA transition.**

### Recommended Action

- **TC-9020**: Consider transitioning to ON_QA. All remediation work is complete.
