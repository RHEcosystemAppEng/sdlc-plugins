# Ready for QA Filtering Analysis

This document details the Ready for QA filtering logic applied to Query 3 results per the triage-security skill's discovery mode protocol.

---

## Query 3 Construction

The third JQL query identifies triaged CVEs that are still in a pre-QA state -- candidates for ON_QA transition once all remediation is complete.

**JQL**:
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

- `labels IN (ai-cve-triaged)` ensures only previously triaged issues are considered
- `status NOT IN (Closed, Verified, 'ON_QA')` excludes issues already closed, verified, or in QA
- Project key `TC` and issue type `10024` are extracted from the Security Configuration in CLAUDE.md

**Raw results**: 3 issues returned.

---

## Filtering Criteria

For each Query 3 result, the skill inspects the issue's `issuelinks` array:

1. **Identify linked remediation Tasks** -- look for `issuelinks` entries where `type.name` is `"Depend"`. Extract linked issue keys from `outwardIssue.key` (or `inwardIssue.key` depending on link direction).
2. **Fetch each linked Task's status** -- determine whether each remediation Task is completed (Done or Closed) or still open.
3. **Apply filtering rules**:
   - **ALL linked remediation Tasks are Done or Closed** --> include in Ready for QA list
   - **ANY linked Task is still open** --> exclude (remediation in progress)
   - **NO linked Tasks with type "Depend" exist** --> exclude (no remediation to verify)

---

## Per-Issue Analysis

### TC-9020 -- CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

| Field | Value |
|-------|-------|
| Status | Modified |
| CVE | CVE-2026-38901 |
| Created | 2026-05-15 |

**Linked Remediation Tasks (Depend)**:

| Task Key | Issue Type | Status | Completed? |
|----------|-----------|--------|------------|
| TC-9021 | Task | Done | Yes |
| TC-9022 | Task | Closed | Yes |

**Filtering result**: **INCLUDED in Ready for QA**

All linked remediation Tasks are in a terminal state (TC-9021 is Done, TC-9022 is Closed). Both meet the "Done or Closed" completion criteria. This CVE's remediation is complete and the issue is a candidate for ON_QA transition.

**Proposed action**: Consider transitioning TC-9020 to ON_QA.

---

### TC-9023 -- CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

| Field | Value |
|-------|-------|
| Status | In Progress |
| CVE | CVE-2026-39102 |
| Created | 2026-05-10 |

**Linked Remediation Tasks (Depend)**:

| Task Key | Issue Type | Status | Completed? |
|----------|-----------|--------|------------|
| TC-9024 | Task | Done | Yes |
| TC-9025 | Task | In Progress | No |

**Filtering result**: **EXCLUDED from Ready for QA**

**Reason**: TC-9025 is still In Progress. Not all linked remediation Tasks are completed -- remediation is still in progress. The ANY-open rule applies: because at least one linked Task (TC-9025) is not Done or Closed, this issue cannot be considered ready for QA.

TC-9024 (Done) has completed its remediation, but TC-9025 remains active. The CVE cannot move to QA until TC-9025 reaches Done or Closed status.

---

### TC-9026 -- CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

| Field | Value |
|-------|-------|
| Status | Modified |
| CVE | CVE-2026-39330 |
| Created | 2026-05-05 |

**Linked Remediation Tasks (Depend)**: None.

**Filtering result**: **EXCLUDED from Ready for QA**

**Reason**: No linked Tasks with type "Depend" exist. Without any linked remediation Tasks, there is no remediation work to verify. This issue may not have had remediation tasks created during triage, or the tasks may have been linked with a different link type. The no-Depend-links rule excludes it from the Ready for QA list.

---

## Summary

| Issue | Status | CVE | Linked Tasks | All Completed? | Ready for QA? | Reason |
|-------|--------|-----|-------------|----------------|---------------|--------|
| TC-9020 | Modified | CVE-2026-38901 | TC-9021 (Done), TC-9022 (Closed) | Yes | **Yes** | All remediation Tasks completed |
| TC-9023 | In Progress | CVE-2026-39102 | TC-9024 (Done), TC-9025 (In Progress) | No | **No** | TC-9025 still In Progress |
| TC-9026 | Modified | CVE-2026-39330 | (none) | N/A | **No** | No Depend links -- no remediation to verify |

**Final Ready for QA list**: 1 issue (TC-9020)

**Proposed transitions**:
- TC-9020: Suggest transitioning to ON_QA -- all remediation is complete.
