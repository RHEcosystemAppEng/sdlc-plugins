# Security Vulnerability Discovery Listing

**Project:** TC
**Vulnerability issue type ID:** 10024
**Jira version prefix:** RHTPA
**Component label pattern:** `pscomponent:`
**Version Streams:** 2.1.x, 2.2.x

---

## 1. Untriaged Issues

**JQL Query:**

```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

**Results: 4 issues**

### Status: New (3 issues)

| # | Issue | CVE ID | Summary | Created |
|---|-------|--------|---------|---------|
| 1 | TC-9001 | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| 2 | TC-9002 | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| 3 | TC-9004 | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |

### Status: In Progress (1 issue)

| # | Issue | CVE ID | Summary | Created |
|---|-------|--------|---------|---------|
| 4 | TC-9003 | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |

---

## 2. Triaged but still New

**JQL Query:**

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

These issues were previously triaged (carry the `ai-cve-triaged` label) but remain in New status, meaning they were never actioned. They may need follow-up or re-triage.

**Results: 1 issue**

| # | Issue | CVE ID | Summary | Created | Labels |
|---|-------|--------|---------|---------|--------|
| 1 | TC-9010 | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 | CVE-2026-39874, pscomponent:org/rhtpa-server, ai-cve-triaged |

---

## 3. Ready for QA

**JQL Query:**

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

After fetching the results, each issue's `issuelinks` are inspected for linked Tasks with link type "Depend". An issue qualifies as Ready for QA only when ALL linked remediation Tasks (Depend type) are Done or Closed. Issues with no Depend links or with any open remediation Tasks are excluded.

**Query returned 3 issues; 1 qualifies as Ready for QA after filtering:**

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

Consider transitioning TC-9020 to ON_QA.

### Excluded from Ready for QA:

| Issue | Status | CVE | Reason for Exclusion |
|-------|--------|-----|----------------------|
| TC-9023 | In Progress | CVE-2026-39102 | Remediation task TC-9025 still In Progress (TC-9024 is Done) |
| TC-9026 | Modified | CVE-2026-39330 | No linked Tasks with Depend type -- no remediation to verify |

---

## Summary

| Category | Count |
|----------|-------|
| Untriaged | 4 |
| Triaged but still New | 1 |
| Ready for QA | 1 (of 3 candidates) |
| **Total issues requiring attention** | **6** |
