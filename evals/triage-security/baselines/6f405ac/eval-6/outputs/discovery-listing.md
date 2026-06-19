# Security Vulnerability Discovery — Project TC

## Configuration Source

Values extracted from Security Configuration in CLAUDE.md:

- **Project key**: TC
- **Vulnerability issue type ID**: 10024
- **Jira version prefix**: RHTPA
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345
- **Version Streams**: 2.1.x, 2.2.x

---

## Query 1: Untriaged Issues

**JQL**:
```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

**4 issues found**, grouped by status:

### Status: New (3 issues)

| # | Key | Status | CVE ID | Summary | Created |
|---|------|--------|--------|---------|---------|
| 1 | TC-9001 | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| 2 | TC-9002 | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| 3 | TC-9004 | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |

### Status: In Progress (1 issue)

| # | Key | Status | CVE ID | Summary | Created |
|---|------|--------|--------|---------|---------|
| 4 | TC-9003 | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |

---

## Query 2: Triaged but still New

**JQL**:
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

**1 issue found**:

| # | Key | Status | CVE ID | Summary | Created |
|---|------|--------|--------|---------|---------|
| 1 | TC-9010 | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

This issue was previously triaged (has `ai-cve-triaged` label) but remains in New status. It may need follow-up or re-triage to determine why it was not actioned.

---

## Summary

- **Total untriaged**: 4 issues (3 New, 1 In Progress)
- **Triaged but stale**: 1 issue (New, never moved forward)
- **Grand total requiring attention**: 5 issues

Select an issue key to begin full triage (Steps 1-7).
