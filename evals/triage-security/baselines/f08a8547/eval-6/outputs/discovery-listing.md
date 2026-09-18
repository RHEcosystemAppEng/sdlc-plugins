# Discovery Mode -- Untriaged Vulnerability Issues

**Project**: TC
**Vulnerability issue type ID**: 10024
**Jira version prefix**: RHTPA
**Component label pattern**: pscomponent:

---

## 1. Untriaged Issues

**JQL Query:**
```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

4 issues found.

### Status: New (3 issues)

| # | Issue | Status | CVE | Summary | Created |
|---|-------|--------|-----|---------|---------|
| 1 | TC-9001 | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| 2 | TC-9002 | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| 3 | TC-9004 | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |

### Status: In Progress (1 issue)

| # | Issue | Status | CVE | Summary | Created |
|---|-------|--------|-----|---------|---------|
| 4 | TC-9003 | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |

---

## 2. Triaged but Still New (stale -- triaged but never actioned)

**JQL Query:**
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

1 issue found.

| # | Issue | Status | CVE | Summary | Created |
|---|-------|--------|-----|---------|---------|
| 1 | TC-9010 | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

These issues have the `ai-cve-triaged` label but remain in New status. They may need follow-up or re-triage.

---

## 3. Ready for QA (triaged CVEs with all remediation tasks completed)

**JQL Query:**
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

3 candidates returned; 1 qualifies as Ready for QA after remediation task filtering.

### Qualified -- Ready for QA

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Task, Done), TC-9022 (Task, Closed) |

All linked remediation Tasks (link type "Depend") are Done or Closed. Consider transitioning TC-9020 to ON_QA.

### Excluded -- Remediation Still in Progress

| Issue | Status | CVE | Summary | Created | Reason |
|-------|--------|-----|---------|---------|--------|
| TC-9023 | In Progress | CVE-2026-39102 | rustls - Certificate validation bypass [rhtpa-2.1] | 2026-05-10 | TC-9025 still In Progress (TC-9024 Done) |

### Excluded -- No Remediation Tasks Linked

| Issue | Status | CVE | Summary | Created | Reason |
|-------|--------|-----|---------|---------|--------|
| TC-9026 | Modified | CVE-2026-39330 | openssl - Buffer overflow in X.509 parsing [rhtpa-2.2] | 2026-05-05 | No linked Tasks with link type "Depend"; no remediation to verify |

---

To triage an issue, provide its key: `/sdlc-workflow:triage-security TC-XXXX`
