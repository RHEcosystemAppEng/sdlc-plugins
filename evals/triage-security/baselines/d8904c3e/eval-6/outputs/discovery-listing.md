# Security Vulnerability Discovery — Project TC

## Configuration Used

- **Project key**: TC
- **Vulnerability issue type ID**: 10024
- **Jira version prefix**: RHTPA

---

## Query 1: Untriaged Issues (primary list)

**JQL**:
```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

4 issues found.

### Status: In Progress

| # | Issue | Status | CVE | Summary | Created |
|---|-------|--------|-----|---------|---------|
| 1 | TC-9003 | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |

### Status: New

| # | Issue | Status | CVE | Summary | Created |
|---|-------|--------|-----|---------|---------|
| 2 | TC-9001 | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| 3 | TC-9002 | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| 4 | TC-9004 | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |

---

## Query 2: Triaged but still New (stale issues)

**JQL**:
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

1 issue found.

These issues were triaged (carry the `ai-cve-triaged` label) but never moved past New status. They may need follow-up or re-triage.

| # | Issue | Status | CVE | Summary | Created |
|---|-------|--------|-----|---------|---------|
| 1 | TC-9010 | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

---

## Query 3: Ready for QA

**JQL**:
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

3 candidates evaluated, 1 qualifies as Ready for QA.

### Ready for QA

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

All linked remediation Tasks are completed. Consider transitioning to ON_QA.

### Excluded from Ready for QA

| Issue | Status | CVE | Summary | Created | Reason |
|-------|--------|-----|---------|---------|--------|
| TC-9023 | In Progress | CVE-2026-39102 | rustls - Certificate validation bypass [rhtpa-2.1] | 2026-05-10 | Remediation in progress: TC-9025 is still In Progress |
| TC-9026 | Modified | CVE-2026-39330 | openssl - Buffer overflow in X.509 parsing [rhtpa-2.2] | 2026-05-05 | No linked remediation Tasks with type "Depend" — no remediation to verify |
