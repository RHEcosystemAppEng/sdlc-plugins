# Security Vulnerability Discovery — Project TC

**Project key:** TC
**Vulnerability issue type ID:** 10024
**Date:** 2026-10-15

---

## Untriaged Vulnerability Issues

4 untriaged Vulnerability issues found in project TC.

### Status: New (3 issues)

1. **TC-9001** | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | Created: 2026-06-08
2. **TC-9002** | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | Created: 2026-06-07
3. **TC-9004** | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | Created: 2026-06-04

### Status: In Progress (1 issue)

4. **TC-9003** | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | Created: 2026-06-05

---

## Triaged but still New

These issues have the `ai-cve-triaged` label but remain in New status. They may need follow-up or re-triage.

1. **TC-9010** | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | Created: 2026-05-28

---

## Ready for QA

Triaged CVEs with all linked remediation Tasks completed. These are candidates for ON_QA transition.

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

**TC-9020**: All linked remediation Tasks are completed. Consider transitioning to ON_QA.

### Excluded from Ready for QA

- **TC-9023** (CVE-2026-39102, In Progress): Remediation task TC-9025 is still In Progress. Not ready for QA.
- **TC-9026** (CVE-2026-39330, Modified): No linked Tasks with type "Depend". No remediation to verify.
