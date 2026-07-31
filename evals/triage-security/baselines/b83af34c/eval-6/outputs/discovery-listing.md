# Discovery Mode — Untriaged Vulnerability Issues

**Project**: TC
**Vulnerability issue type ID**: 10024
**Configuration source**: Security Configuration in CLAUDE.md

---

## 1. Untriaged Issues

**JQL Query**:
```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

### Status: New

1. **TC-9001** | Status: New | CVE: CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | Created: 2026-06-08
2. **TC-9002** | Status: New | CVE: CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | Created: 2026-06-07
3. **TC-9004** | Status: New | CVE: CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | Created: 2026-06-04

### Status: In Progress

4. **TC-9003** | Status: In Progress | CVE: CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | Created: 2026-06-05

---

## 2. Triaged but still New

**JQL Query**:
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

These issues were previously triaged (carry the `ai-cve-triaged` label) but remain in New status. They may need follow-up or re-triage.

1. **TC-9010** | Status: New | CVE: CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | Created: 2026-05-28

---

## 3. Ready for QA

**JQL Query**:
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

After filtering by linked remediation Task status (all "Depend"-linked Tasks must be Done or Closed):

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

Consider transitioning TC-9020 to ON_QA.

### Excluded from Ready for QA

- **TC-9023** (CVE-2026-39102, In Progress): Excluded -- TC-9025 is still In Progress. Remediation is not yet complete.
- **TC-9026** (CVE-2026-39330, Modified): Excluded -- no linked Tasks with type "Depend" exist. No remediation to verify.
