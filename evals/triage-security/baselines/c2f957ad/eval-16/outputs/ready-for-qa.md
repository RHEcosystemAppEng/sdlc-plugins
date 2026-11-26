# Ready for QA — Filtering Analysis

## Query

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged)
  AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
fields: summary, labels, status, created, issuelinks   maxResults: 20
```

The query returned 3 candidates: TC-9020, TC-9023, TC-9026.

## Filtering rules (SKILL.md, Discovery mode, Query 3)

For each candidate, look at `issuelinks` entries where `type.name == "Depend"`. Take the linked Task key from `outwardIssue.key` or `inwardIssue.key` and check that Task's status. Then apply these rules:

1. If **ALL** Depend-linked Tasks are Done or Closed, the issue is **included** (Ready for QA).
2. If **ANY** Depend-linked Task is still open, the issue is **excluded** (remediation in progress).
3. If there are **no** Depend-linked Tasks, the issue is **excluded** (no remediation to verify).

## Per-issue evaluation

### TC-9020: QUALIFIED (Ready for QA)

- CVE: CVE-2026-38901 (hyper - HTTP request smuggling) [rhtpa-2.2]
- Current status: Modified
- Depend links:

| Linked Task | Type | Status | Completed? |
|-------------|------|--------|------------|
| TC-9021 | Task | Done | Yes |
| TC-9022 | Task | Closed | Yes |

- Rule hit: **Rule 1**. TC-9020 has 2 Depend-linked Tasks and both are completed (Done or Closed).
- Result: **Included.** Suggestion: "Consider transitioning to ON_QA."

### TC-9023: EXCLUDED (remediation in progress)

- CVE: CVE-2026-39102 (rustls - Certificate validation bypass) [rhtpa-2.1]
- Current status: In Progress
- Depend links:

| Linked Task | Type | Status | Completed? |
|-------------|------|--------|------------|
| TC-9024 | Task | Done | Yes |
| TC-9025 | Task | In Progress | **No** |

- Rule hit: **Rule 2**. TC-9025 is still open (In Progress). TC-9024 is Done, but that is not enough: the rule requires every linked Task to be complete.
- Result: **Excluded.** Remediation is still going on, so the issue is not ready for ON_QA.

### TC-9026: EXCLUDED (no remediation to verify)

- CVE: CVE-2026-39330 (openssl - Buffer overflow in X.509 parsing) [rhtpa-2.2]
- Current status: Modified
- Depend links: **none**
- Rule hit: **Rule 3**. TC-9026 has no linked Tasks with type "Depend".
- Result: **Excluded.** There is no remediation to verify. Its status is Modified even though it has no Depend-linked remediation Tasks. It may be worth a manual check, for example whether the remediation was tracked through a different link type or handled outside Jira.

## Summary

| Issue | CVE | Status | Depend-linked Tasks | Decision | Reason |
|-------|-----|--------|---------------------|----------|--------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | **Ready for QA** | All remediation Tasks completed |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | Excluded | TC-9025 still open |
| TC-9026 | CVE-2026-39330 | Modified | (none) | Excluded | No Depend links |

**Ready for QA list:** TC-9020. Consider transitioning to ON_QA.

The skill made no Jira changes. The ON_QA transition is only a suggestion and needs explicit engineer confirmation before anything is done.
