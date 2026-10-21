# Security Vulnerability Discovery — Project TC

Discovery mode invoked without an issue key. Listing untriaged and triaged Vulnerability issues.

**Project key:** TC
**Vulnerability issue type ID:** 10024
**Jira version prefix:** RHTPA

---

## Untriaged Vulnerability Issues

**JQL:** `project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC`

4 issues found.

### Status: New

| # | Issue | CVE | Summary | Created |
|---|-------|-----|---------|---------|
| 1 | TC-9001 | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| 2 | TC-9002 | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| 3 | TC-9004 | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |

### Status: In Progress

| # | Issue | CVE | Summary | Created |
|---|-------|-----|---------|---------|
| 4 | TC-9003 | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |

> **Note:** TC-9003 is already In Progress. It may be actively worked on. Consider verifying whether triage is needed or if work is already underway.

---

## Triaged but still New

**JQL:** `project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC`

1 issue found.

| # | Issue | CVE | Summary | Created |
|---|-------|-----|---------|---------|
| 1 | TC-9010 | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

> **Flag:** These issues were triaged (carry `ai-cve-triaged` label) but remain in New status. They may need follow-up or re-triage to move forward.

---

## Ready for QA

**JQL:** `project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC`

3 candidates evaluated; **1 qualified** as Ready for QA.

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

> Consider transitioning TC-9020 to ON_QA.

### Excluded from Ready for QA

| Issue | Status | CVE | Reason for Exclusion |
|-------|--------|-----|----------------------|
| TC-9023 | In Progress | CVE-2026-39102 | Remediation in progress -- TC-9025 is still In Progress |
| TC-9026 | Modified | CVE-2026-39330 | No linked remediation Tasks with type "Depend" -- no remediation to verify |

---

Select an issue key to begin triage, or specify a Ready for QA issue to transition to ON_QA.
