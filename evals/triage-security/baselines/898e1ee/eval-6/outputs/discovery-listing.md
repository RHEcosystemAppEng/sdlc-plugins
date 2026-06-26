# Security Vulnerability Discovery — Project TC

No issue key was provided. Running discovery mode to list untriaged and stale Vulnerability issues.

## Configuration Used

- **Project key**: TC
- **Vulnerability issue type ID**: 10024
- **Component label pattern**: pscomponent:

---

## Query 1: Untriaged Issues

**JQL**:
```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

4 issues found.

### Status: In Progress

| # | Issue Key | Status | CVE ID | Summary | Created |
|---|-----------|--------|--------|---------|---------|
| 1 | TC-9003 | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |

### Status: New

| # | Issue Key | Status | CVE ID | Summary | Created |
|---|-----------|--------|--------|---------|---------|
| 2 | TC-9001 | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| 3 | TC-9002 | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| 4 | TC-9004 | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |

---

## Query 2: Triaged but still New

**JQL**:
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

1 issue found. These issues were previously triaged (carry the `ai-cve-triaged` label) but remain in New status, which may indicate they need follow-up or re-triage.

| # | Issue Key | Status | CVE ID | Summary | Created |
|---|-----------|--------|--------|---------|---------|
| 1 | TC-9010 | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

---

**Total**: 5 Vulnerability issues found (4 untriaged, 1 triaged-but-stale).

Select an issue key to begin triage, or specify an action.
