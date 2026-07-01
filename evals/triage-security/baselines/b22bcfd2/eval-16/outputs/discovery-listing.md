# Discovery Mode — Untriaged Vulnerability Issues

**Project**: TC
**Vulnerability issue type ID**: 10024
**Date**: 2026-07-01

---

## Step 0 — Configuration Validation

Extracted from Security Configuration in CLAUDE.md:

- **Project key**: TC
- **Vulnerability issue type ID**: 10024
- **Jira version prefix**: RHTPA
- **Component label pattern**: `pscomponent:`

These values are used to construct the JQL queries below.

---

## Query 1: Untriaged Issues

**JQL**:
```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

**Results** (4 issues):

### Status: New

1. **TC-9001** | Status: New | CVE: CVE-2026-40112 | Summary: h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | Created: 2026-06-08
2. **TC-9002** | Status: New | CVE: CVE-2026-40297 | Summary: serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | Created: 2026-06-07
3. **TC-9004** | Status: New | CVE: CVE-2026-40518 | Summary: ring - Timing side-channel in RSA verification [rhtpa-2.2] | Created: 2026-06-04

### Status: In Progress

4. **TC-9003** | Status: In Progress | CVE: CVE-2026-40455 | Summary: tokio - Race condition in task cancellation [rhtpa-2.2] | Created: 2026-06-05

#### Status-aware handling:

- **TC-9001** (New): Ready for full triage.
- **TC-9002** (New): Ready for full triage.
- **TC-9004** (New): Ready for full triage.
- **TC-9003** (In Progress): **Warning** — This issue is already in `In Progress`. It may be actively worked on. Options: (1) Proceed with triage anyway, (2) Skip this issue.

---

## Query 2: Triaged but still New

**JQL**:
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

**Results** (1 issue):

1. **TC-9010** | Status: New | CVE: CVE-2026-39874 | Summary: quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | Created: 2026-05-28

> These issues were triaged (labeled `ai-cve-triaged`) but remain in `New` status. They may need follow-up or re-triage.

---

## Query 3: Ready for QA Candidates

**JQL**:
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

**Results** (3 issues returned, filtered by linked remediation Task completion):

For each result, the skill checks `issuelinks` for linked Tasks with link type `Depend` and fetches each linked Task's status to determine readiness.

### Ready for QA

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

> **TC-9020**: All linked remediation Tasks are completed (TC-9021 Done, TC-9022 Closed). Consider transitioning to ON_QA.

### Excluded from Ready for QA

| Issue | Status | CVE | Summary | Created | Reason | Remediation Tasks |
|-------|--------|-----|---------|---------|--------|-------------------|
| TC-9023 | In Progress | CVE-2026-39102 | rustls - Certificate validation bypass [rhtpa-2.1] | 2026-05-10 | TC-9025 still In Progress | TC-9024 (Done), TC-9025 (In Progress) |
| TC-9026 | Modified | CVE-2026-39330 | openssl - Buffer overflow in X.509 parsing [rhtpa-2.2] | 2026-05-05 | No Depend links | (none) |

---

To triage a specific issue, run: `/sdlc-workflow:triage-security TC-XXXX`
