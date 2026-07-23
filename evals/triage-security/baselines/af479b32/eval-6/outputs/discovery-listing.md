# Discovery Mode — Vulnerability Issue Listing

## Configuration Used

| Parameter | Value | Source |
|-----------|-------|--------|
| Project key | TC | Jira Configuration |
| Vulnerability issue type ID | 10024 | Security Configuration > Product Lifecycle |
| Component label pattern | pscomponent: | Security Configuration > Product Lifecycle |
| Jira version prefix | RHTPA | Security Configuration > Product Lifecycle |

---

## Query 1: Untriaged Issues

**JQL:**

```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

**Results: 4 issues**

### Status: New (3 issues)

| # | Issue | CVE ID | Summary | Created |
|---|-------|--------|---------|---------|
| 1 | TC-9001 | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| 2 | TC-9002 | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| 3 | TC-9004 | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |

### Status: In Progress (1 issue)

| # | Issue | CVE ID | Summary | Created |
|---|-------|--------|---------|---------|
| 4 | TC-9003 | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |

---

## Query 2: Triaged but still New (stale issues)

**JQL:**

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

These issues were previously triaged (carry the `ai-cve-triaged` label) but remain in New status, meaning they were never actioned. They may need follow-up or re-triage.

**Results: 1 issue**

### Status: New (1 issue)

| # | Issue | CVE ID | Summary | Created |
|---|-------|--------|---------|---------|
| 1 | TC-9010 | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

---

## Query 3: Ready for QA Candidates

**JQL:**

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

For each result, linked Tasks with link type "Depend" were inspected to determine readiness:

- ALL linked remediation Tasks Done or Closed --> Ready for QA
- ANY linked Task still open --> Excluded (remediation in progress)
- NO linked Tasks with type "Depend" --> Excluded (no remediation to verify)

**Results: 3 issues evaluated, 1 ready for QA**

### Ready for QA (1 issue)

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

Recommendation: Consider transitioning TC-9020 to ON_QA. All linked remediation tasks are complete.

### Excluded (2 issues)

| Issue | Status | CVE | Summary | Reason |
|-------|--------|-----|---------|--------|
| TC-9023 | In Progress | CVE-2026-39102 | rustls - Certificate validation bypass [rhtpa-2.1] | Remediation in progress: TC-9025 still In Progress |
| TC-9026 | Modified | CVE-2026-39330 | openssl - Buffer overflow in X.509 parsing [rhtpa-2.2] | No linked remediation Tasks with type "Depend" |

---

## Summary

| Category | Count |
|----------|-------|
| Untriaged | 4 |
| Triaged but still New (stale) | 1 |
| Ready for QA | 1 |
| **Total issues found** | **6** |
