# Discovery Mode — Vulnerability Issue Listing

## Step 0 — Configuration Extraction

From the project's CLAUDE.md Security Configuration:

- **Project key**: TC
- **Vulnerability issue type ID**: 10024
- **Jira version prefix**: RHTPA
- **Component label pattern**: pscomponent:

These values are used to construct the JQL queries below.

---

## Query 1: Untriaged Issues

**JQL Query:**
```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

**Results** (4 issues):

### Status: New

1. **TC-9001** — Status: New — CVE: CVE-2026-40112 — Summary: CVE-2026-40112 h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] — Created: 2026-06-08
2. **TC-9002** — Status: New — CVE: CVE-2026-40297 — Summary: CVE-2026-40297 serde_json - Stack overflow on deeply nested input [rhtpa-2.1] — Created: 2026-06-07
3. **TC-9004** — Status: New — CVE: CVE-2026-40518 — Summary: CVE-2026-40518 ring - Timing side-channel in RSA verification [rhtpa-2.2] — Created: 2026-06-04

### Status: In Progress

4. **TC-9003** — Status: In Progress — CVE: CVE-2026-40455 — Summary: CVE-2026-40455 tokio - Race condition in task cancellation [rhtpa-2.2] — Created: 2026-06-05

---

## Query 2: Triaged but still New

**JQL Query:**
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

**Results** (1 issue):

1. **TC-9010** — Status: New — CVE: CVE-2026-39874 — Summary: CVE-2026-39874 quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] — Created: 2026-05-28

> This issue was triaged (ai-cve-triaged label present) but remains in New status. It may need follow-up or re-triage.

---

## Query 3: Ready for QA

**JQL Query:**
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

**Raw results** (3 issues). After filtering by linked remediation Task completion status:

### Ready for QA — Qualified Issues

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

> Consider transitioning TC-9020 to ON_QA — all linked remediation Tasks are completed.

### Excluded from Ready for QA

| Issue | Status | CVE | Summary | Reason | Details |
|-------|--------|-----|---------|--------|---------|
| TC-9023 | In Progress | CVE-2026-39102 | rustls - Certificate validation bypass [rhtpa-2.1] | Remediation in progress | TC-9024 (Done), TC-9025 (In Progress) — TC-9025 is still In Progress |
| TC-9026 | Modified | CVE-2026-39330 | openssl - Buffer overflow in X.509 parsing [rhtpa-2.2] | No remediation tasks | No linked Tasks with type "Depend" — no remediation to verify |

### Filtering Logic

For each Query 3 result, the skill checks `issuelinks` for linked Tasks with link type "Depend" and fetches each linked Task's status:

- **TC-9020**: ALL linked remediation Tasks completed (TC-9021 Done, TC-9022 Closed) → **Included** in Ready for QA
- **TC-9023**: TC-9025 is still In Progress → **Excluded** (remediation is not complete)
- **TC-9026**: No linked Tasks with type "Depend" → **Excluded** (no remediation to verify)
