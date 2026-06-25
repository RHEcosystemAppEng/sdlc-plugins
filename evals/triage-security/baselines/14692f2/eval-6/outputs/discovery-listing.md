# Discovery Mode: Untriaged Vulnerability Issues

**Project**: TC
**Vulnerability Issue Type ID**: 10024

---

## 1. Untriaged Issues

**JQL Query**:
```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

**Results (4 issues)**:

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

## 2. Triaged but still New

**JQL Query**:
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

These issues were previously triaged (carry the `ai-cve-triaged` label) but remain in **New** status, meaning they were never actioned. They may need follow-up or re-triage.

**Results (1 issue)**:

| # | Key | Status | CVE ID | Summary | Created |
|---|-----|--------|--------|---------|---------|
| 1 | TC-9010 | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

---

**Total**: 5 Vulnerability issues found (4 untriaged, 1 triaged but still New).

Select an issue key to begin triage, or specify an action.
