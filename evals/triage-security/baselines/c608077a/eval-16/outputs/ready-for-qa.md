# Ready for QA Filtering Analysis

## Query

```
jira.search_jql(
  jql: "project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC",
  fields: ["summary", "labels", "status", "created", "issuelinks"],
  maxResults: 20
)
```

The query returned 3 candidates: TC-9020, TC-9023 and TC-9026.

## Filtering rules (from SKILL.md, Discovery mode, query 3)

For each candidate, look at the `issuelinks` entries whose `type.name == "Depend"`. Take the linked issue key from `outwardIssue.key` or `inwardIssue.key`, then fetch that linked Task's status.

1. If every linked "Depend" Task is **Done or Closed**, the issue is **included** in Ready for QA.
2. If **any** linked "Depend" Task is still open, the issue is **excluded** because remediation is still in progress.
3. If there are **no** "Depend" links, the issue is **excluded** because there is no remediation to verify.

## Per-issue evaluation

| Issue | CVE | Status | Depend-linked Tasks | Task statuses | All Done or Closed? | Rule | Result |
|-------|-----|--------|---------------------|---------------|---------------------|------|--------|
| TC-9020 | CVE-2026-38901 (hyper) | Modified | TC-9021, TC-9022 | Done, Closed | Yes (2 of 2) | 1 | **Ready for QA** |
| TC-9023 | CVE-2026-39102 (rustls) | In Progress | TC-9024, TC-9025 | Done, In Progress | No (1 of 2) | 2 | **Excluded** |
| TC-9026 | CVE-2026-39330 (openssl) | Modified | (none) | n/a | n/a | 3 | **Excluded** |

### TC-9020: qualifies
- Summary: hyper - HTTP request smuggling [rhtpa-2.2]
- Depend links: TC-9021 (Task, **Done**) and TC-9022 (Task, **Closed**).
- Both linked remediation Tasks count as complete (Done and Closed are both terminal states), so rule 1 applies.
- **Recommendation:** Consider transitioning to ON_QA.

### TC-9023: excluded (remediation in progress)
- Summary: rustls - Certificate validation bypass [rhtpa-2.1]
- Depend links: TC-9024 (Task, Done) and TC-9025 (Task, **In Progress**).
- TC-9025 is still open. One open Task is enough to exclude the issue under rule 2, even though TC-9024 is Done.
- Re-check once TC-9025 reaches Done or Closed.

### TC-9026: excluded (no remediation to verify)
- Summary: openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]
- It has no issue links of type "Depend", so rule 3 applies.
- Its status is Modified even though no remediation Tasks are linked. Look into this manually: the links may be missing, or the fix may have been tracked outside the triage workflow. It should not move to ON_QA until there is remediation to verify.

## Result

- **Ready for QA (1):** TC-9020. Suggestion: "Consider transitioning to ON_QA."
- **Excluded (2):** TC-9023 (Task TC-9025 still open) and TC-9026 (no Depend-linked remediation Tasks).

No Jira transitions or other changes were made. This is a read-only discovery listing, and any ON_QA transition needs the engineer to confirm it.
