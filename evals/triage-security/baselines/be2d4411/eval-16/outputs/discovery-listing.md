# Security Vulnerability Discovery — Project TC

## Untriaged Issues

**JQL**: `project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC`

**4 issues found**, grouped by status:

### New (3)

1. **TC-9001** | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08
2. **TC-9002** | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07
3. **TC-9004** | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04

### In Progress (1)

4. **TC-9003** | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05

---

## Triaged but still New

**JQL**: `project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC`

These issues were previously triaged (labeled `ai-cve-triaged`) but remain in New status. They may need follow-up or re-triage.

**1 issue found:**

1. **TC-9010** | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28

---

## Ready for QA

**JQL**: `labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, ON_QA)`

Triaged CVEs where all linked remediation Tasks (Depend link type) are completed (Done or Closed). These are candidates for transition to ON_QA.

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

**Suggested action for TC-9020:** Consider transitioning to ON_QA. All linked remediation tasks have been completed.

### Excluded from Ready for QA

- **TC-9023** (CVE-2026-39102, In Progress) — Excluded: TC-9025 still In Progress. Remediation is incomplete.
- **TC-9026** (CVE-2026-39330, Modified) — Excluded: No linked Tasks with Depend link type. No remediation to verify.
