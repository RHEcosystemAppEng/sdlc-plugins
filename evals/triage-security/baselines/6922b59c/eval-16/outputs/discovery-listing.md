# Security Vulnerability Discovery — Project TC

**Project key:** TC
**Vulnerability issue type ID:** 10024
**Jira version prefix:** RHTPA
**Component label pattern:** `pscomponent:`

---

## Untriaged Issues (4)

Issues without the `ai-cve-triaged` label, ordered by status then created date descending.

### In Progress

1. **TC-9003** | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | Created: 2026-06-05

### New

2. **TC-9001** | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | Created: 2026-06-08
3. **TC-9002** | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | Created: 2026-06-07
4. **TC-9004** | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | Created: 2026-06-04

---

## Triaged but still New (1)

Issues with the `ai-cve-triaged` label that remain in New status. These may need follow-up or re-triage.

1. **TC-9010** | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | Created: 2026-05-28

---

## Ready for QA (1)

Triaged CVEs where all linked remediation Tasks (link type "Depend") are Done or Closed. These are candidates for ON_QA transition.

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

Consider transitioning TC-9020 to ON_QA.

---

## Summary

- **4** untriaged Vulnerability issues awaiting triage
- **1** triaged issue still in New status (may need follow-up)
- **1** issue ready for QA transition (all remediation complete)
