# Discovery Mode — Untriaged Vulnerability Issues

## Step 0 — Configuration Extraction

Extracted from CLAUDE.md Security Configuration:
- **Project key**: TC
- **Vulnerability issue type ID**: 10024
- **Jira version prefix**: RHTPA
- **Component label pattern**: pscomponent:

---

## Query 1: Untriaged Issues

**JQL**:
```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

**Results** (4 issues):

### Status: New

1. **TC-9001** — `New` — CVE-2026-40112 — CVE-2026-40112 h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] — Created: 2026-06-08
   - *Ready for full triage*

2. **TC-9002** — `New` — CVE-2026-40297 — CVE-2026-40297 serde_json - Stack overflow on deeply nested input [rhtpa-2.1] — Created: 2026-06-07
   - *Ready for full triage*

3. **TC-9004** — `New` — CVE-2026-40518 — CVE-2026-40518 ring - Timing side-channel in RSA verification [rhtpa-2.2] — Created: 2026-06-04
   - *Ready for full triage*

### Status: In Progress

4. **TC-9003** — `In Progress` — CVE-2026-40455 — CVE-2026-40455 tokio - Race condition in task cancellation [rhtpa-2.2] — Created: 2026-06-05
   - **Warning**: This issue is already in `In Progress`. It may be actively worked on. Proceeding with triage may conflict with active work. Options: (1) Proceed with triage anyway, (2) Skip this issue.

### Status-aware handling summary

| Issue | Status | Handling |
|-------|--------|----------|
| TC-9001 | New | Proceed with full triage |
| TC-9002 | New | Proceed with full triage |
| TC-9004 | New | Proceed with full triage |
| TC-9003 | In Progress | Warning — may be actively worked on |

---

## Query 2: Triaged but still New

**JQL**:
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

**Results** (1 issue):

1. **TC-9010** — `New` — CVE-2026-39874 — CVE-2026-39874 quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] — Created: 2026-05-28
   - *Flagged: This issue was triaged (has `ai-cve-triaged` label) but status is still New. It was never moved forward. May need follow-up or re-triage.*

---

## Query 3: Ready for QA Candidates

**JQL**:
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

**Results** (3 issues returned, filtered by linked remediation Task completion):

For each result, the skill checks `issuelinks` for linked Tasks with link type "Depend" and fetches each linked Task's status to determine readiness.

### Ready for QA

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

> Consider transitioning TC-9020 to ON_QA. All linked remediation tasks are completed.

### Excluded from Ready for QA

| Issue | Status | CVE | Summary | Exclusion Reason | Remediation Tasks |
|-------|--------|-----|---------|------------------|-------------------|
| TC-9023 | In Progress | CVE-2026-39102 | rustls - Certificate validation bypass [rhtpa-2.1] | TC-9025 still In Progress — remediation not complete | TC-9024 (Done), TC-9025 (In Progress) |
| TC-9026 | Modified | CVE-2026-39330 | openssl - Buffer overflow in X.509 parsing [rhtpa-2.2] | No linked Tasks with type "Depend" — no remediation to verify | (none) |
