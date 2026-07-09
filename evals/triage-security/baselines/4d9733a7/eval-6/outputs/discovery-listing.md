# Discovery Mode -- Issue Listing

No issue key was provided. Running discovery mode using the Security Configuration from CLAUDE.md.

## Configuration Values Used

- **Project key**: TC (from Jira Configuration)
- **Vulnerability issue type ID**: 10024 (from Security Configuration > Product Lifecycle)

---

## Query 1: Untriaged Issues

**JQL query constructed**:
```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

**Results** (4 issues):

| # | Issue | Status | CVE ID | Summary | Created |
|---|-------|--------|--------|---------|---------|
| 1 | TC-9001 | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| 2 | TC-9002 | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| 3 | TC-9004 | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |
| 4 | TC-9003 | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |

> **Warning**: TC-9003 is already in `In Progress` status. It may be actively worked on. If selected, you will be asked whether to proceed with triage anyway or skip this issue.

---

## Query 2: Triaged but still New

**JQL query constructed**:
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

**Results** (1 issue):

| # | Issue | Status | CVE ID | Summary | Created |
|---|-------|--------|--------|---------|---------|
| 1 | TC-9010 | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

> **Note**: This issue was previously triaged (has `ai-cve-triaged` label) but remains in New status. It may need follow-up or re-triage.

---

## Query 3: Ready for QA Candidates

**JQL query constructed**:
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

**Results** (3 issues returned, filtered by linked remediation Task completion):

For each result, the skill checks `issuelinks` for linked Tasks with link type "Depend" and fetches each linked Task's status:

### Filtering Analysis

**TC-9020** (CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]):
- Status: Modified
- Linked remediation Tasks:
  - TC-9021 (Task) -- Status: **Done**
  - TC-9022 (Task) -- Status: **Closed**
- Result: ALL linked remediation Tasks are completed --> **READY FOR QA**

**TC-9023** (CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]):
- Status: In Progress
- Linked remediation Tasks:
  - TC-9024 (Task) -- Status: Done
  - TC-9025 (Task) -- Status: **In Progress**
- Result: TC-9025 is still In Progress --> **EXCLUDED** (remediation not complete)

**TC-9026** (CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]):
- Status: Modified
- Linked remediation Tasks: (no Depend links)
- Result: No linked Tasks with type "Depend" --> **EXCLUDED** (no remediation to verify)

### Ready for QA Table

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

> Consider transitioning TC-9020 to ON_QA -- all linked remediation tasks are completed.

### Excluded Issues

| Issue | Status | CVE | Reason for Exclusion |
|-------|--------|-----|---------------------|
| TC-9023 | In Progress | CVE-2026-39102 | TC-9025 still In Progress -- remediation not complete |
| TC-9026 | Modified | CVE-2026-39330 | No Depend links -- no remediation to verify |

---

Select an issue to begin triage, or type a specific issue key.
