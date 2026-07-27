# Discovery Mode — Untriaged Vulnerability Issues

**Project**: TC
**Vulnerability issue type ID**: 10024

---

## Query 1: Untriaged Issues

**JQL**:
```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

**Results** (4 issues):

### Status: New

1. **TC-9001** — CVE-2026-40112 h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2]
   - Status: New
   - CVE: CVE-2026-40112
   - Created: 2026-06-08
   - *Ready for full triage.*

2. **TC-9002** — CVE-2026-40297 serde_json - Stack overflow on deeply nested input [rhtpa-2.1]
   - Status: New
   - CVE: CVE-2026-40297
   - Created: 2026-06-07
   - *Ready for full triage.*

3. **TC-9004** — CVE-2026-40518 ring - Timing side-channel in RSA verification [rhtpa-2.2]
   - Status: New
   - CVE: CVE-2026-40518
   - Created: 2026-06-04
   - *Ready for full triage.*

### Status: In Progress

4. **TC-9003** — CVE-2026-40455 tokio - Race condition in task cancellation [rhtpa-2.2]
   - Status: In Progress
   - CVE: CVE-2026-40455
   - Created: 2026-06-05
   - **Warning**: This issue is already in `In Progress`. It may be actively worked on. Proceed with caution or skip.

---

## Query 2: Triaged but still New

**JQL**:
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

**Results** (1 issue):

1. **TC-9010** — CVE-2026-39874 quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2]
   - Status: New
   - CVE: CVE-2026-39874
   - Created: 2026-05-28
   - *Flagged: This issue was previously triaged (ai-cve-triaged label present) but remains in New status. It may need follow-up or re-triage.*

---

## Query 3: Ready for QA

**JQL**:
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

This query finds triaged CVEs that are still in a pre-QA state. For each result, the linked remediation Tasks (link type "Depend") are inspected to determine if all remediation work is complete.

**Filtering criteria**:
- ALL linked remediation Tasks must be Done or Closed to qualify
- ANY linked Task still open (not Done/Closed) disqualifies the issue
- NO linked Tasks with type "Depend" disqualifies the issue (no remediation to verify)

### Qualified for Ready for QA

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

> **Suggestion**: Consider transitioning TC-9020 to ON_QA. All linked remediation Tasks are completed.

### Excluded from Ready for QA

| Issue | Status | CVE | Summary | Reason | Details |
|-------|--------|-----|---------|--------|---------|
| TC-9023 | In Progress | CVE-2026-39102 | rustls - Certificate validation bypass [rhtpa-2.1] | Remediation in progress | TC-9025 is still In Progress (TC-9024 is Done) |
| TC-9026 | Modified | CVE-2026-39330 | openssl - Buffer overflow in X.509 parsing [rhtpa-2.2] | No remediation to verify | No linked Tasks with type "Depend" |
