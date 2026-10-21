# Discovery Mode — Untriaged Vulnerability Issue Listing

**Project**: TC
**Vulnerability issue type ID**: 10024
**Jira version prefix**: RHTPA
**Version Streams**: 2.1.x, 2.2.x

---

## Query 1: Untriaged Issues (primary list)

**JQL**:
```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

**Results**: 4 issues

### Status: In Progress

| # | Issue | CVE ID | Summary | Created |
|---|-------|--------|---------|---------|
| 1 | TC-9003 | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |

### Status: New

| # | Issue | CVE ID | Summary | Created |
|---|-------|--------|---------|---------|
| 2 | TC-9001 | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| 3 | TC-9002 | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| 4 | TC-9004 | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |

---

## Query 2: Triaged but still New (stale issues)

**JQL**:
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

**Results**: 1 issue

These issues were previously triaged (carry the `ai-cve-triaged` label) but remain in New status. They may need follow-up or re-triage.

| # | Issue | CVE ID | Summary | Created |
|---|-------|--------|---------|---------|
| 1 | TC-9010 | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

---

## Query 3: Ready for QA

**JQL**:
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

**Candidates returned**: 3 issues

**Filtering criteria**: A triaged CVE is Ready for QA only when ALL linked remediation Tasks (link type "Depend") are Done or Closed. Issues with any open Task or no Depend links are excluded.

### Ready for QA

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

Consider transitioning TC-9020 to ON_QA.

### Excluded from Ready for QA

| Issue | Status | CVE | Summary | Reason |
|-------|--------|-----|---------|--------|
| TC-9023 | In Progress | CVE-2026-39102 | rustls - Certificate validation bypass [rhtpa-2.1] | TC-9025 still In Progress (remediation in progress) |
| TC-9026 | Modified | CVE-2026-39330 | openssl - Buffer overflow in X.509 parsing [rhtpa-2.2] | No linked Tasks with type "Depend" (no remediation to verify) |

---

## Query 4: Release Jira Summary

**JQL**:
```
project = TC AND issuetype = Task AND summary ~ 'RHTPA' AND summary ~ 'CVE triage' ORDER BY created DESC
```

**Results**: No release Tasks returned in discovery data.

No release Jira summary is available. If release Tasks exist, they would be listed here with remediation progress counts (CVEs tracked, remediation done, remediation pending) per release version.
