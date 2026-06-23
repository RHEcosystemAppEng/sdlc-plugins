# Discovery Mode: Untriaged Vulnerability Issues

**Project**: TC
**Vulnerability Issue Type ID**: 10024
**Jira Version Prefix**: RHTPA
**Date**: 2026-06-23

---

## Query 1: Untriaged Issues

**JQL constructed from Security Configuration:**

```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

- `project = TC` -- from Jira Configuration: Project key
- `issuetype = 10024` -- from Security Configuration > Product Lifecycle: Vulnerability issue type ID
- `labels NOT IN (ai-cve-triaged)` -- filters out previously triaged issues
- `ORDER BY status ASC, created DESC` -- groups by status, newest first within each group

**Results: 4 issues**

### Status: New (3 issues)

| # | Issue Key | CVE ID | Summary | Stream | Created |
|---|-----------|--------|---------|--------|---------|
| 1 | TC-9001 | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability | rhtpa-2.2 (stream 2.2.x) | 2026-06-08 |
| 2 | TC-9002 | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input | rhtpa-2.1 (stream 2.1.x) | 2026-06-07 |
| 3 | TC-9004 | CVE-2026-40518 | ring - Timing side-channel in RSA verification | rhtpa-2.2 (stream 2.2.x) | 2026-06-04 |

### Status: In Progress (1 issue)

| # | Issue Key | CVE ID | Summary | Stream | Created |
|---|-----------|--------|---------|--------|---------|
| 4 | TC-9003 | CVE-2026-40455 | tokio - Race condition in task cancellation | rhtpa-2.2 (stream 2.2.x) | 2026-06-05 |

---

## Query 2: Triaged but still New (stale issues)

**JQL constructed from Security Configuration:**

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

- `project = TC` -- from Jira Configuration: Project key
- `issuetype = 10024` -- from Security Configuration > Product Lifecycle: Vulnerability issue type ID
- `labels IN (ai-cve-triaged)` -- only issues already triaged by this skill
- `status = New` -- triaged but never moved to In Progress or beyond
- `ORDER BY created DESC` -- newest first

**Results: 1 issue**

| # | Issue Key | CVE ID | Summary | Stream | Created | Flag |
|---|-----------|--------|---------|--------|---------|------|
| 1 | TC-9010 | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame | rhtpa-2.2 (stream 2.2.x) | 2026-05-28 | Triaged but never actioned -- may need follow-up or re-triage |

---

## Summary

- **4 untriaged** Vulnerability issues awaiting triage (3 New, 1 In Progress)
- **1 stale** issue that was previously triaged but remains in New status (TC-9010, created 26 days ago)
- All issues are scoped to streams **2.1.x** or **2.2.x**, matching the configured Version Streams
- Stream 2.2.x has the highest concentration: 3 untriaged + 1 stale issue
- Stream 2.1.x has 1 untriaged issue

### Stream Distribution

| Stream | Untriaged | Stale (triaged but New) | Total |
|--------|-----------|------------------------|-------|
| 2.1.x  | 1         | 0                      | 1     |
| 2.2.x  | 3         | 1                      | 4     |
| **Total** | **4**  | **1**                  | **5** |
