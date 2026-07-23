# Security Vulnerability Discovery — Project TC

## Step 0 — Configuration Validated

| Setting | Value |
|---------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Vulnerability issue type ID | 10024 |
| Jira version prefix | RHTPA |
| Component label pattern | pscomponent: |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| VEX Justification field | customfield_12345 |

---

## Untriaged Vulnerability Issues (4 issues)

Issues without the `ai-cve-triaged` label, ordered by status then created date.

### Status: New (3 issues)

| # | Issue | CVE | Summary | Created |
|---|-------|-----|---------|---------|
| 1 | TC-9001 | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| 2 | TC-9002 | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| 3 | TC-9004 | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |

### Status: In Progress (1 issue)

| # | Issue | CVE | Summary | Created |
|---|-------|-----|---------|---------|
| 4 | TC-9003 | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |

---

## Triaged but still New (1 issue)

These issues have the `ai-cve-triaged` label but remain in New status. They may need follow-up or re-triage.

| # | Issue | CVE | Summary | Created |
|---|-------|-----|---------|---------|
| 1 | TC-9010 | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

---

## Ready for QA (1 issue)

Triaged CVEs where all linked remediation Tasks (link type "Depend") are Done or Closed. These are candidates for ON_QA transition.

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

Consider transitioning TC-9020 to ON_QA.

### Excluded from Ready for QA

| Issue | Status | Reason |
|-------|--------|--------|
| TC-9023 | In Progress | Remediation in progress -- TC-9025 is still In Progress |
| TC-9026 | Modified | No linked Tasks with type "Depend" -- no remediation to verify |

---

To triage a specific issue, run: `/sdlc-workflow:triage-security TC-XXXX`
