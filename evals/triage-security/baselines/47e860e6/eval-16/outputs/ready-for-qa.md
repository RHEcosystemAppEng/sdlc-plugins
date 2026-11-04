# Ready for QA — Filtering Analysis

## Query

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged)
  AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

Fields: summary, labels, status, created, issuelinks (maxResults 20)

The query returned 3 candidates.

## Filtering rules (from SKILL.md, Discovery mode, Query 3)

For each candidate, look only at `issuelinks` entries where `type.name == "Depend"`. Take the linked issue key from `outwardIssue.key` or `inwardIssue.key`, depending on link direction, and check that Task's status.

1. **ALL** Depend-linked Tasks are Done or Closed: **include** (ready for the ON_QA transition).
2. **ANY** Depend-linked Task is still open: **exclude** (remediation still in progress).
3. **NO** Depend-linked Tasks: **exclude** (no remediation to verify).

## Per-issue evaluation

### TC-9020: CVE-2026-38901, hyper (HTTP request smuggling) [rhtpa-2.2]

- Status: Modified (not Closed/Verified/ON_QA, so it is a valid candidate)
- Labels: CVE-2026-38901, pscomponent:org/rhtpa-server, ai-cve-triaged
- Depend links:

| Linked Task | Type | Status | Completed? |
|---|---|---|---|
| TC-9021 | Task | Done | Yes |
| TC-9022 | Task | Closed | Yes |

- Result: rule 1 applies, since both of its 2 Depend-linked Tasks are Done or Closed.
- **Decision: INCLUDED (Ready for QA).** Recommendation: consider transitioning to ON_QA.

### TC-9023: CVE-2026-39102, rustls (Certificate validation bypass) [rhtpa-2.1]

- Status: In Progress
- Labels: CVE-2026-39102, pscomponent:org/rhtpa-server, ai-cve-triaged
- Depend links:

| Linked Task | Type | Status | Completed? |
|---|---|---|---|
| TC-9024 | Task | Done | Yes |
| TC-9025 | Task | In Progress | **No** |

- Result: rule 2 applies, because TC-9025 is still open. One completed Task (TC-9024) is not enough when another is still open.
- **Decision: EXCLUDED.** Remediation is still in progress. Re-check after TC-9025 is Done or Closed.

### TC-9026: CVE-2026-39330, openssl (Buffer overflow in X.509 parsing) [rhtpa-2.2]

- Status: Modified
- Labels: CVE-2026-39330, pscomponent:org/rhtpa-server, ai-cve-triaged
- Depend links: **none**
- Result: rule 3 applies, as there are no remediation Tasks to verify.
- **Decision: EXCLUDED.** No remediation to verify. Being in Modified status does not qualify an issue on its own; the rule depends on linked Depend Tasks, not on the CVE's own status. The engineer may want to check why a triaged issue in Modified has no Depend-linked remediation Tasks. For example, the fix may be tracked through a Related or preemptive link, or the remediation link may be missing.

## Summary

| Issue | CVE | Status | Depend-linked Tasks | Open Tasks | Decision |
|---|---|---|---|---|---|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | 0 | **Ready for QA** |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | 1 | Excluded (remediation in progress) |
| TC-9026 | CVE-2026-39330 | Modified | none | — | Excluded (no remediation to verify) |

**Ready for QA list:** TC-9020 (1 of 3 candidates).

## Ready for QA table (as presented to the engineer)

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

For TC-9020: consider transitioning to ON_QA.

No Jira mutation was performed. Discovery mode only lists issues. Any ON_QA transition needs the engineer's explicit confirmation, and the target status would be resolved from that issue's live workflow transitions rather than a hardcoded ID.
