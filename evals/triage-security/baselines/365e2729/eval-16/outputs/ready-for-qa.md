# Ready for QA — Filtering Analysis

## Query

```
jira.search_jql(
  jql: "project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC",
  fields: ["summary", "labels", "status", "created", "issuelinks"],
  maxResults: 20
)
```

The query returned 3 candidates: TC-9020, TC-9023 and TC-9026.

## Filtering Rules (SKILL.md, Discovery mode, query 3)

For each candidate, look at the `issuelinks` entries whose `type.name` is `"Depend"`. Get the linked issue key from `outwardIssue.key` or `inwardIssue.key`, then fetch that Task's status. Then apply these rules:

1. **All** Depend-linked Tasks are Done or Closed: **include** in Ready for QA.
2. **Any** Depend-linked Task is still open: **exclude**, because remediation is in progress.
3. There are **no** Depend-linked Tasks: **exclude**, because there is no remediation to verify.

## Per-Issue Evaluation

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- Current status: Modified (not Closed, Verified or ON_QA, so it is a valid candidate)
- Depend links:

  | Linked Task | Type | Status | Completed? |
  |-------------|------|--------|------------|
  | TC-9021 | Task | Done | Yes |
  | TC-9022 | Task | Closed | Yes |

- Rule applied: Rule 1. Both linked remediation Tasks are completed.
- **Result: QUALIFIES (Ready for QA)**
- Suggestion: "Consider transitioning to ON_QA."

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- Current status: In Progress
- Depend links:

  | Linked Task | Type | Status | Completed? |
  |-------------|------|--------|------------|
  | TC-9024 | Task | Done | Yes |
  | TC-9025 | Task | In Progress | **No** |

- Rule applied: Rule 2. One linked Task (TC-9025) is still open.
- **Result: EXCLUDED** (remediation still in progress)

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- Current status: Modified
- Depend links: none
- Rule applied: Rule 3. No Depend-linked remediation Tasks exist.
- **Result: EXCLUDED** (no remediation to verify)
- Note: the issue is in Modified even though it has no Depend-linked remediation Tasks. This may be worth checking by hand. The fix might be tracked through some other link type, or the links may be missing.

## Summary

| Issue | CVE | Status | Depend Tasks | All Completed? | Outcome |
|-------|-----|--------|--------------|----------------|---------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | **Ready for QA** |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | Excluded (remediation in progress) |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A | Excluded (no remediation to verify) |

Of the 3 candidates, 1 qualified: **TC-9020**.

Recommendation: consider transitioning TC-9020 to ON_QA. This listing does not change anything in Jira. Discovery mode only reports the issue so an engineer can make the transition.
