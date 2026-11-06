# Ready for QA: Filtering Analysis

## Query

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

Fields: `summary, labels, status, created, issuelinks` (maxResults 20). The query returned 3 candidates.

## Filtering rules (SKILL.md, Discovery mode, Query 3)

For each candidate, look at its `issuelinks` entries where `type.name == "Depend"`. Read the linked issue key from `outwardIssue.key` or `inwardIssue.key`, then fetch that issue's status.

| Rule | Condition | Result |
|------|-----------|--------|
| R1 | ALL linked "Depend" remediation Tasks are Done or Closed | **Include** (Ready for QA) |
| R2 | ANY linked "Depend" Task is still open | **Exclude** (remediation in progress) |
| R3 | NO linked Tasks with link type "Depend" | **Exclude** (no remediation to verify) |

## Per-issue evaluation

### TC-9020: CVE-2026-38901 hyper, HTTP request smuggling [rhtpa-2.2]

- Status: Modified. Labels include `ai-cve-triaged`. Created 2026-05-15.
- Depend links:

  | Linked Task | Type | Status | Completed? |
  |-------------|------|--------|-----------|
  | TC-9021 | Task | Done | Yes |
  | TC-9022 | Task | Closed | Yes |

- Rule applied: **R1**. Both linked remediation Tasks (2 of 2) are in a terminal state, Done or Closed.
- **Result: INCLUDED. Ready for QA.**
- Recommendation: Consider transitioning to ON_QA.

### TC-9023: CVE-2026-39102 rustls, certificate validation bypass [rhtpa-2.1]

- Status: In Progress. Labels include `ai-cve-triaged`. Created 2026-05-10.
- Depend links:

  | Linked Task | Type | Status | Completed? |
  |-------------|------|--------|-----------|
  | TC-9024 | Task | Done | Yes |
  | TC-9025 | Task | In Progress | **No** |

- Rule applied: **R2**. One of the 2 linked remediation Tasks is still open (TC-9025 is In Progress).
- **Result: EXCLUDED. Remediation is still in progress.**
- Re-check once TC-9025 reaches Done or Closed.

### TC-9026: CVE-2026-39330 openssl, buffer overflow in X.509 parsing [rhtpa-2.2]

- Status: Modified. Labels include `ai-cve-triaged`. Created 2026-05-05.
- Depend links: none.
- Rule applied: **R3**. No linked Tasks use the "Depend" link type.
- **Result: EXCLUDED. There is no remediation to verify.**
- Worth reviewing by hand: the issue is labeled triaged and is in Modified status, but it has no Depend-linked remediation Tasks. Possible reasons:
  - Remediation was done outside the tracked Task workflow.
  - The work is tracked through a different link type, such as Related (preemptive tasks) or a cross-CVE dedup link to another CVE's task.
  - The links were never created.

  The skill does not infer readiness from non-Depend links, so this issue is not suggested for ON_QA.

## Summary

| Issue | CVE | Status | Depend Tasks | Done/Closed | Open | Rule | Result |
|-------|-----|--------|--------------|-------------|------|------|--------|
| TC-9020 | CVE-2026-38901 | Modified | 2 | 2 | 0 | R1 | **Ready for QA** |
| TC-9023 | CVE-2026-39102 | In Progress | 2 | 1 | 1 (TC-9025) | R2 | Excluded (remediation in progress) |
| TC-9026 | CVE-2026-39330 | Modified | 0 | 0 | 0 | R3 | Excluded (no remediation to verify) |

**Ready for QA list:** 1 issue, TC-9020. Suggested action: consider transitioning TC-9020 to ON_QA.

No Jira changes were made. Discovery mode only lists issues. Any ON_QA transition needs a separate action that the engineer explicitly confirms.
