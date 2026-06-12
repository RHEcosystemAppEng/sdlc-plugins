# Vulnerability Issue Discovery — Project TC

Discovery mode: listing untriaged and stale Vulnerability issues.

**Configuration used:**
- Project key: `TC`
- Vulnerability issue type ID: `10024`

---

## Untriaged Issues

**JQL:** `project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC`

4 issues found.

### Status: In Progress

| # | Key | Status | CVE ID | Summary | Created |
|---|-----|--------|--------|---------|---------|
| 1 | TC-9003 | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |

### Status: New

| # | Key | Status | CVE ID | Summary | Created |
|---|-----|--------|--------|---------|---------|
| 2 | TC-9001 | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| 3 | TC-9002 | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| 4 | TC-9004 | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |

---

## Triaged but still New

These issues have been previously triaged (labeled `ai-cve-triaged`) but remain in `New` status. They may need follow-up or re-triage.

**JQL:** `project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC`

1 issue found.

| # | Key | Status | CVE ID | Summary | Created |
|---|-----|--------|--------|---------|---------|
| 1 | TC-9010 | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

---

To triage a specific issue, invoke: `/sdlc-workflow:triage-security <issue-key>` (e.g., `/sdlc-workflow:triage-security TC-9001`).
