# Discovery Mode — Vulnerability Issue Listing

No issue key was provided. Running discovery mode to list Vulnerability issues
in project **TC** using vulnerability issue type ID **10024** (extracted from
Security Configuration in CLAUDE.md).

---

## Query 1: Untriaged Issues

**JQL query constructed from Security Configuration:**

```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

- `TC` — Project key from Jira Configuration
- `10024` — Vulnerability issue type ID from Security Configuration

**Results (4 issues):**

### New

1. **TC-9001** | Status: New | CVE: CVE-2026-40112
   Summary: CVE-2026-40112 h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2]
   Created: 2026-06-08

2. **TC-9002** | Status: New | CVE: CVE-2026-40297
   Summary: CVE-2026-40297 serde_json - Stack overflow on deeply nested input [rhtpa-2.1]
   Created: 2026-06-07

3. **TC-9004** | Status: New | CVE: CVE-2026-40518
   Summary: CVE-2026-40518 ring - Timing side-channel in RSA verification [rhtpa-2.2]
   Created: 2026-06-04

### In Progress

4. **TC-9003** | Status: In Progress | CVE: CVE-2026-40455
   Summary: CVE-2026-40455 tokio - Race condition in task cancellation [rhtpa-2.2]
   Created: 2026-06-05

---

## Query 2: Triaged but still New

**JQL query constructed from Security Configuration:**

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

These issues were triaged (have the `ai-cve-triaged` label) but remain in New
status — they may need follow-up or re-triage.

**Results (1 issue):**

1. **TC-9010** | Status: New | CVE: CVE-2026-39874
   Summary: CVE-2026-39874 quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2]
   Created: 2026-05-28

---

## Query 3: Ready for QA

**JQL query constructed from Security Configuration:**

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

This query returns triaged CVEs that are not yet in a terminal or QA state.
For each result, linked remediation Tasks (link type "Depend") are inspected
to determine whether all remediation is complete.

**Raw results (3 issues) — filtered by linked Task completion status:**

### Qualified for Ready for QA

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

All linked remediation Tasks for TC-9020 are completed (TC-9021: Done,
TC-9022: Closed). Consider transitioning TC-9020 to ON_QA.

### Excluded from Ready for QA

| Issue | Status | CVE | Summary | Reason for Exclusion |
|-------|--------|-----|---------|----------------------|
| TC-9023 | In Progress | CVE-2026-39102 | rustls - Certificate validation bypass [rhtpa-2.1] | Remediation in progress: TC-9025 is still In Progress (TC-9024 is Done) |
| TC-9026 | Modified | CVE-2026-39330 | openssl - Buffer overflow in X.509 parsing [rhtpa-2.2] | No linked Tasks with type "Depend" — no remediation to verify |
