# Discovery Mode: Untriaged Vulnerability Issues

**Project:** TC
**Vulnerability issue type ID:** 10024
**Jira version prefix:** RHTPA
**Date:** 2026-06-30

---

## Query 1: Untriaged Issues

**JQL:**
```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

**Results:** 4 issues

### Status: In Progress

1. **TC-9003** | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | Created: 2026-06-05

### Status: New

2. **TC-9001** | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | Created: 2026-06-08
3. **TC-9002** | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | Created: 2026-06-07
4. **TC-9004** | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | Created: 2026-06-04

---

## Query 2: Triaged but still New

**JQL:**
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

**Results:** 1 issue

These issues were triaged (carry the `ai-cve-triaged` label) but remain in New status -- they may need follow-up or re-triage.

1. **TC-9010** | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | Created: 2026-05-28

---

## Query 3: Ready for QA

**JQL:**
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

**Results:** 3 candidates evaluated, 1 qualifies as Ready for QA

For each candidate, the linked remediation Tasks (link type "Depend") were inspected to determine readiness:

- **TC-9020**: ALL linked remediation Tasks completed (TC-9021 Done, TC-9022 Closed) -- **Ready for QA**
- **TC-9023**: TC-9025 still In Progress -- **Excluded** (remediation in progress)
- **TC-9026**: No linked Tasks with type "Depend" -- **Excluded** (no remediation to verify)

### Ready for QA Issues

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

**Recommendation for TC-9020:** Consider transitioning to ON_QA. All linked remediation tasks are completed.

### Excluded from Ready for QA

| Issue | Status | CVE | Summary | Created | Reason |
|-------|--------|-----|---------|---------|--------|
| TC-9023 | In Progress | CVE-2026-39102 | rustls - Certificate validation bypass [rhtpa-2.1] | 2026-05-10 | TC-9025 still In Progress |
| TC-9026 | Modified | CVE-2026-39330 | openssl - Buffer overflow in X.509 parsing [rhtpa-2.2] | 2026-05-05 | No Depend-linked tasks |

---

Select an issue key to begin triage, or enter a specific issue key directly.
