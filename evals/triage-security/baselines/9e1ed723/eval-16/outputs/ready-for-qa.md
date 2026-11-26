# Ready for QA Filtering Analysis

## Source query (Query 3)

```
jira.search_jql(
  jql: "project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC",
  fields: ["summary", "labels", "status", "created", "issuelinks"],
  maxResults: 20
)
```

Query 3 returned 3 candidates: TC-9020, TC-9023 and TC-9026.

## Filtering rules (SKILL.md, Discovery mode, step 3)

For each candidate, look at the `issuelinks` entries whose `type.name` is `"Depend"`. Take the linked issue key from `outwardIssue.key` or `inwardIssue.key` and fetch that issue's status.

1. **ALL** linked "Depend" Tasks are Done or Closed: **include** (Ready for QA).
2. **ANY** linked "Depend" Task is still open: **exclude** (remediation in progress).
3. **NO** "Depend" links exist: **exclude** (no remediation to verify).

## Per-issue evaluation

### TC-9020: CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- Status: Modified (not Closed, Verified or ON_QA, so it is a valid candidate)
- Labels: CVE-2026-38901, pscomponent:org/rhtpa-server, ai-cve-triaged
- "Depend" links:
  | Linked Issue | Type | Status | Completed? |
  |---|---|---|---|
  | TC-9021 | Task | Done | Yes |
  | TC-9022 | Task | Closed | Yes |
- Rule applied: rule 1. All 2 of 2 linked remediation Tasks are Done or Closed.
- **Result: QUALIFIES. Ready for QA.**
- Recommendation: Consider transitioning to ON_QA.

### TC-9023: CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- Status: In Progress
- Labels: CVE-2026-39102, pscomponent:org/rhtpa-server, ai-cve-triaged
- "Depend" links:
  | Linked Issue | Type | Status | Completed? |
  |---|---|---|---|
  | TC-9024 | Task | Done | Yes |
  | TC-9025 | Task | In Progress | **No** |
- Rule applied: rule 2. 1 of 2 linked Tasks (TC-9025) is still open.
- **Result: EXCLUDED. Remediation is still in progress.**
- It would become a candidate once TC-9025 reaches Done or Closed.

### TC-9026: CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- Status: Modified
- Labels: CVE-2026-39330, pscomponent:org/rhtpa-server, ai-cve-triaged
- "Depend" links: none
- Rule applied: rule 3. No linked Tasks with link type "Depend".
- **Result: EXCLUDED. There is no remediation to verify.**
- Note: the issue is in Modified status but has no remediation Tasks linked. Check whether the remediation Tasks were never created or were linked with a different link type. It may need re-triage or manual linking before it can move to ON_QA.

## Summary

| Issue | CVE | Status | Depend-linked Tasks | Rule | Outcome |
|-------|-----|--------|---------------------|------|---------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | All complete | **Ready for QA** |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | One open | Excluded: remediation in progress |
| TC-9026 | CVE-2026-39330 | Modified | (none) | No Depend links | Excluded: no remediation to verify |

**Ready for QA list (presented to the engineer):**

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

TC-9020: Consider transitioning to ON_QA.

No transitions were made. Discovery mode only lists and suggests issues; the engineer decides whether to move TC-9020 to ON_QA.
