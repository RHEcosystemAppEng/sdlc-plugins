# Security Vulnerability Discovery — Project TC

## Configuration

- **Project key**: TC
- **Vulnerability issue type ID**: 10024
- **Component label pattern**: `pscomponent:`
- **Jira version prefix**: RHTPA

---

## Untriaged Vulnerability Issues

4 issues found matching: `project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC`

### In Progress

| # | Issue | Status | CVE | Summary | Created |
|---|-------|--------|-----|---------|---------|
| 1 | TC-9003 | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |

### New

| # | Issue | Status | CVE | Summary | Created |
|---|-------|--------|-----|---------|---------|
| 2 | TC-9001 | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| 3 | TC-9002 | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| 4 | TC-9004 | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |

---

## Triaged but Still New (Stale)

1 issue found matching: `project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC`

These issues were previously triaged (`ai-cve-triaged` label present) but remain in New status. They may need follow-up or re-triage.

| # | Issue | Status | CVE | Summary | Created |
|---|-------|--------|-----|---------|---------|
| 1 | TC-9010 | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

---

## Ready for QA

Triaged CVEs with all linked remediation tasks completed. These are candidates for transition to ON_QA.

Query: `project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC`

3 candidates evaluated, **1 qualified**:

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

Consider transitioning TC-9020 to ON_QA.

### Excluded from Ready for QA

| Issue | Status | CVE | Reason |
|-------|--------|-----|--------|
| TC-9023 | In Progress | CVE-2026-39102 | Remediation in progress -- TC-9025 is still In Progress |
| TC-9026 | Modified | CVE-2026-39330 | No linked Tasks with type "Depend" -- no remediation to verify |

---

To triage a specific issue, run: `/sdlc-workflow:triage-security <issue-key>`
