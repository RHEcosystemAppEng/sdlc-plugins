# Security Vulnerability Discovery — Project TC

**Discovery mode** — no issue key provided. Listing untriaged, stale, and Ready for QA Vulnerability issues.

**Configuration validated:**
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Vulnerability issue type ID: 10024
- Jira version prefix: RHTPA
- Component label pattern: pscomponent:

---

## Untriaged Issues (4)

Issues without the `ai-cve-triaged` label, ordered by status then created date descending.

### Status: New (3)

| # | Issue | Status | CVE | Summary | Created |
|---|-------|--------|-----|---------|---------|
| 1 | TC-9001 | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| 2 | TC-9002 | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| 3 | TC-9004 | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |

### Status: In Progress (1)

| # | Issue | Status | CVE | Summary | Created |
|---|-------|--------|-----|---------|---------|
| 4 | TC-9003 | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |

> To triage any of these issues, run `/triage-security <issue-key>` (e.g., `/triage-security TC-9001`).

---

## Triaged but Still New (1)

Issues with `ai-cve-triaged` label that remain in New status. These were triaged but never actioned and may need follow-up or re-triage.

| # | Issue | Status | CVE | Summary | Created |
|---|-------|--------|-----|---------|---------|
| 1 | TC-9010 | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

> These issues were previously triaged (ai-cve-triaged label present) but remain in New status. Consider re-triaging or manually advancing them.

---

## Ready for QA (1)

Triaged CVEs where **all** linked remediation Tasks (link type "Depend") are Done or Closed. These are candidates for transition to ON_QA.

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

> **Proposed action for TC-9020:** Consider transitioning to ON_QA. All linked remediation tasks are complete.

### Excluded from Ready for QA

| Issue | Status | CVE | Reason |
|-------|--------|-----|--------|
| TC-9023 | In Progress | CVE-2026-39102 | Remediation in progress: TC-9025 is still In Progress |
| TC-9026 | Modified | CVE-2026-39330 | No linked Tasks with type "Depend" exist (no remediation to verify) |

---

**Summary:** 4 untriaged issues awaiting triage, 1 stale triaged issue in New status, 1 issue ready for QA transition.
