# Discovery Mode: Untriaged Vulnerability Issues

**Project:** TC
**Vulnerability Issue Type ID:** 10024
**Component Label Pattern:** `pscomponent:`
**Jira Version Prefix:** RHTPA

---

## Query 1: Untriaged Issues

**JQL:**
```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

4 issues found, grouped by status:

### Status: New (3 issues)

| # | Issue | Status | CVE ID | Summary | Created |
|---|-------|--------|--------|---------|---------|
| 1 | TC-9001 | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| 2 | TC-9002 | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| 3 | TC-9004 | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |

### Status: In Progress (1 issue)

| # | Issue | Status | CVE ID | Summary | Created |
|---|-------|--------|--------|---------|---------|
| 4 | TC-9003 | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |

---

## Query 2: Triaged but still New (stale issues)

**JQL:**
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

1 issue found. These issues were previously triaged (have `ai-cve-triaged` label) but remain in New status -- they may need follow-up or re-triage.

| # | Issue | Status | CVE ID | Summary | Created |
|---|-------|--------|--------|---------|---------|
| 1 | TC-9010 | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

---

## Query 3: Ready for QA

**JQL:**
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

3 candidate issues found. After filtering by linked remediation task completion:

### Ready for QA (1 issue)

All linked remediation Tasks (link type "Depend") are Done or Closed.

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

Consider transitioning TC-9020 to ON_QA.

### Excluded from Ready for QA (2 issues)

| Issue | Status | CVE | Summary | Reason |
|-------|--------|-----|---------|--------|
| TC-9023 | In Progress | CVE-2026-39102 | rustls - Certificate validation bypass [rhtpa-2.1] | Remediation in progress: TC-9025 is still In Progress |
| TC-9026 | Modified | CVE-2026-39330 | openssl - Buffer overflow in X.509 parsing [rhtpa-2.2] | No linked Tasks with link type "Depend" -- no remediation to verify |
