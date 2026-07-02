# Security Vulnerability Discovery — Project TC

No issue key was provided. Running discovery mode to list untriaged and actionable Vulnerability issues.

**Security Configuration extracted from CLAUDE.md:**
- Project key: **TC**
- Vulnerability issue type ID: **10024**
- Jira version prefix: **RHTPA**
- Component label pattern: **pscomponent:**
- VEX Justification custom field: **customfield_12345**

---

## 1. Untriaged Issues

**JQL query:**
```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

4 issues found, grouped by status:

### Status: New (3 issues)

1. **TC-9001** | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | Created: 2026-06-08
2. **TC-9002** | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | Created: 2026-06-07
3. **TC-9004** | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | Created: 2026-06-04

### Status: In Progress (1 issue)

4. **TC-9003** | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | Created: 2026-06-05

---

## 2. Triaged but still New (stale)

These issues were previously triaged (carry the `ai-cve-triaged` label) but remain in New status -- they may need follow-up or re-triage.

**JQL query:**
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

1 issue found:

1. **TC-9010** | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | Created: 2026-05-28

---

## 3. Ready for QA

Triaged CVEs where all linked remediation Tasks (link type "Depend") are completed (Done or Closed). These are candidates for transition to ON_QA.

**JQL query:**
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

3 candidates returned; after filtering by remediation task completion:

### Qualifies for ON_QA (1 issue)

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

All linked remediation Tasks are completed. Consider transitioning TC-9020 to ON_QA.

### Excluded (2 issues)

| Issue | Status | CVE | Summary | Reason for Exclusion |
|-------|--------|-----|---------|----------------------|
| TC-9023 | In Progress | CVE-2026-39102 | rustls - Certificate validation bypass [rhtpa-2.1] | Remediation in progress -- TC-9025 is still In Progress (TC-9024 is Done) |
| TC-9026 | Modified | CVE-2026-39330 | openssl - Buffer overflow in X.509 parsing [rhtpa-2.2] | No linked Tasks with type "Depend" -- no remediation to verify |
