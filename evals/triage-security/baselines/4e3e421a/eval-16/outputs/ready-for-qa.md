# Ready for QA Filtering Analysis

## Query

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
fields: summary, labels, status, created, issuelinks
maxResults: 20
```

The query returned 3 candidates: TC-9020, TC-9023 and TC-9026.

## Filtering Rules (from SKILL.md, Discovery mode Query 3)

For each candidate, check `issuelinks` for entries where `type.name == "Depend"`. Then check the status of each linked Task:

1. **All** linked Depend Tasks are Done or Closed: **include** in Ready for QA.
2. **Any** linked Depend Task is still open: **exclude**, because remediation is still in progress.
3. **No** Depend links: **exclude**, because there is no remediation to verify.

## Per-Issue Evaluation

### TC-9020 (CVE-2026-38901, hyper: HTTP request smuggling [rhtpa-2.2])

- Current status: Modified
- Depend-linked Tasks:

  | Task | Type | Status | Completed? |
  |------|------|--------|------------|
  | TC-9021 | Task | Done | Yes |
  | TC-9022 | Task | Closed | Yes |

- Rule applied: rule 1. Both linked remediation Tasks are Done or Closed.
- **Result: QUALIFIES for Ready for QA.**
- Recommendation: Consider transitioning to ON_QA.

### TC-9023 (CVE-2026-39102, rustls: Certificate validation bypass [rhtpa-2.1])

- Current status: In Progress
- Depend-linked Tasks:

  | Task | Type | Status | Completed? |
  |------|------|--------|------------|
  | TC-9024 | Task | Done | Yes |
  | TC-9025 | Task | In Progress | **No** |

- Rule applied: rule 2. TC-9025 is still open (In Progress). Having one Task done (TC-9024) is not enough; every linked Task must be completed.
- **Result: EXCLUDED.** Remediation is still in progress.

### TC-9026 (CVE-2026-39330, openssl: Buffer overflow in X.509 parsing [rhtpa-2.2])

- Current status: Modified
- Depend-linked Tasks: none
- Rule applied: rule 3. With no Depend links, there is no remediation to verify. A Modified status alone is not enough to qualify.
- **Result: EXCLUDED.** There is no remediation to verify. It may be worth checking manually why a triaged CVE in Modified status has no linked remediation Tasks. For example, the links may have been Related or preemptive links, or remediation may have happened outside Jira.

## Summary

| Issue | CVE | Status | Depend Tasks | Outcome | Reason |
|-------|-----|--------|--------------|---------|--------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | **Ready for QA** | All remediation Tasks completed |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | Excluded | TC-9025 still open |
| TC-9026 | CVE-2026-39330 | Modified | none | Excluded | No Depend-linked remediation Tasks |

**Ready for QA list:** TC-9020. Consider transitioning it to ON_QA.

No Jira changes were made. Any ON_QA transition needs the engineer to confirm it first.
