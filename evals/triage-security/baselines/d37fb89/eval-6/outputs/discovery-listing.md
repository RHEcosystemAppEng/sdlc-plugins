# Discovery Mode: Untriaged Vulnerability Issues

**Project**: TC
**Vulnerability Issue Type ID**: 10024
**Date**: 2026-06-23

---

## Query 1: Untriaged Issues

**JQL**:
```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

**4 issues found**, grouped by status:

### Status: New (3 issues)

| # | Key | CVE ID | Summary | Created |
|---|-----|--------|---------|---------|
| 1 | TC-9001 | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| 2 | TC-9002 | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| 3 | TC-9004 | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |

### Status: In Progress (1 issue)

| # | Key | CVE ID | Summary | Created |
|---|-----|--------|---------|---------|
| 4 | TC-9003 | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |

---

## Query 2: Triaged but still New

**JQL**:
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

**1 issue found**:

| # | Key | CVE ID | Summary | Labels | Created |
|---|-----|--------|---------|--------|---------|
| 1 | TC-9010 | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | ai-cve-triaged | 2026-05-28 |

This issue was previously triaged (has `ai-cve-triaged` label) but remains in **New** status. It may need follow-up or re-triage to determine why it has not progressed.

---

## Summary

- **3 untriaged issues in New status** -- ready for full triage
- **1 untriaged issue in In Progress status** -- already being worked; triage may still be useful for version impact verification
- **1 triaged issue still in New status** -- may be stale; consider follow-up

Select an issue key to begin triage, or re-triage a previously triaged issue.
