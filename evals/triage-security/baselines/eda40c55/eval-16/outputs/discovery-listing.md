# Security Vulnerability Discovery — Project TC

**Project**: TC | **Vulnerability issue type**: 10024 | **Date**: 2026-07-06

---

## 1. Untriaged Issues

*JQL*: `project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC`

**4 issues found.**

### Status: New

| # | Issue | CVE | Summary | Created |
|---|-------|-----|---------|---------|
| 1 | TC-9001 | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| 2 | TC-9002 | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| 3 | TC-9004 | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |

### Status: In Progress

| # | Issue | CVE | Summary | Created |
|---|-------|-----|---------|---------|
| 4 | TC-9003 | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |

---

## 2. Triaged but still New

*JQL*: `project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC`

**1 issue found.** These issues were triaged but never moved forward and may need follow-up or re-triage.

| # | Issue | CVE | Summary | Created |
|---|-------|-----|---------|---------|
| 1 | TC-9010 | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

---

## 3. Ready for QA

*JQL*: `project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC`

**3 candidates evaluated, 1 qualified.**

Triaged CVEs where all linked remediation Tasks (link type "Depend") are Done or Closed. These are candidates for transition to ON_QA.

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

> **Recommendation**: Consider transitioning TC-9020 to ON_QA. All linked remediation tasks have been completed.

### Excluded from Ready for QA

| Issue | Status | CVE | Reason |
|-------|--------|-----|--------|
| TC-9023 | In Progress | CVE-2026-39102 | Remediation in progress -- TC-9025 is still In Progress |
| TC-9026 | Modified | CVE-2026-39330 | No linked remediation Tasks (no Depend links) |
