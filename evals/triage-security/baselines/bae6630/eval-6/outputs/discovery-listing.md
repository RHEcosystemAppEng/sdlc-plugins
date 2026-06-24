# Security Vulnerability Discovery — Project TC

## Configuration Used

| Setting | Value |
|---------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Vulnerability issue type ID | 10024 |
| Jira version prefix | RHTPA |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Version Streams | 2.1.x, 2.2.x |

---

## Untriaged Vulnerability Issues

**JQL Query:**
```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

**Results: 4 issues**

### Status: New (3 issues)

1. **TC-9001** | Status: New | CVE-2026-40112
   - Summary: CVE-2026-40112 h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2]
   - Component: pscomponent:org/rhtpa-server
   - Created: 2026-06-08

2. **TC-9002** | Status: New | CVE-2026-40297
   - Summary: CVE-2026-40297 serde_json - Stack overflow on deeply nested input [rhtpa-2.1]
   - Component: pscomponent:org/rhtpa-server
   - Created: 2026-06-07

3. **TC-9004** | Status: New | CVE-2026-40518
   - Summary: CVE-2026-40518 ring - Timing side-channel in RSA verification [rhtpa-2.2]
   - Component: pscomponent:org/rhtpa-server
   - Created: 2026-06-04

### Status: In Progress (1 issue)

4. **TC-9003** | Status: In Progress | CVE-2026-40455
   - Summary: CVE-2026-40455 tokio - Race condition in task cancellation [rhtpa-2.2]
   - Component: pscomponent:org/rhtpa-server
   - Created: 2026-06-05

---

## Triaged but still New (stale — triaged but never actioned)

**JQL Query:**
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

**Results: 1 issue**

1. **TC-9010** | Status: New | CVE-2026-39874
   - Summary: CVE-2026-39874 quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2]
   - Component: pscomponent:org/rhtpa-server
   - Labels: CVE-2026-39874, pscomponent:org/rhtpa-server, ai-cve-triaged
   - Created: 2026-05-28
   - **Note:** This issue was previously triaged (has `ai-cve-triaged` label) but remains in New status. It may need follow-up or re-triage.
