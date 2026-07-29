# Security Vulnerability Discovery Listing

**Project**: TC
**Vulnerability Issue Type ID**: 10024
**Jira Version Prefix**: RHTPA
**Component Label Pattern**: `pscomponent:`
**Configured Streams**: 2.1.x, 2.2.x

---

## 1. Untriaged Issues

**JQL Query**:
```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

4 issues found, grouped by status:

### Status: New (3 issues)

1. **TC-9001** | New | CVE-2026-40112
   h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2]
   Created: 2026-06-08

2. **TC-9002** | New | CVE-2026-40297
   serde_json - Stack overflow on deeply nested input [rhtpa-2.1]
   Created: 2026-06-07

3. **TC-9004** | New | CVE-2026-40518
   ring - Timing side-channel in RSA verification [rhtpa-2.2]
   Created: 2026-06-04

### Status: In Progress (1 issue)

4. **TC-9003** | In Progress | CVE-2026-40455
   tokio - Race condition in task cancellation [rhtpa-2.2]
   Created: 2026-06-05

---

## 2. Triaged but still New

**JQL Query**:
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

1 issue found:

1. **TC-9010** | New | CVE-2026-39874
   quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2]
   Created: 2026-05-28
   Labels: CVE-2026-39874, pscomponent:org/rhtpa-server, ai-cve-triaged

   **Flag**: This issue was triaged (has `ai-cve-triaged` label) but remains in New status. It may need follow-up or re-triage -- it was triaged but never moved forward.

---

## 3. Ready for QA

**JQL Query**:
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

3 candidates returned; after filtering on linked remediation Task completion:

| Issue | Status | CVE | Summary | Created | Remediation Tasks | Ready? |
|-------|--------|-----|---------|---------|-------------------|--------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) | Yes |
| TC-9023 | In Progress | CVE-2026-39102 | rustls - Certificate validation bypass [rhtpa-2.1] | 2026-05-10 | TC-9024 (Done), TC-9025 (In Progress) | No |
| TC-9026 | Modified | CVE-2026-39330 | openssl - Buffer overflow in X.509 parsing [rhtpa-2.2] | 2026-05-05 | (no Depend links) | No |

### Filtering rationale

- **TC-9020**: ALL linked remediation Tasks are completed (TC-9021 Done, TC-9022 Closed). **Ready for QA.** Consider transitioning to ON_QA.
- **TC-9023**: Excluded -- TC-9025 is still In Progress. Remediation is not yet complete.
- **TC-9026**: Excluded -- no linked Tasks with link type "Depend" exist. No remediation to verify.

### Ready for QA summary

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

Consider transitioning TC-9020 to ON_QA.
