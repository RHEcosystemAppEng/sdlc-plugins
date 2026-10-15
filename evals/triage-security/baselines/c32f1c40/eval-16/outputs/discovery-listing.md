# Discovery Mode — Vulnerability Issue Listing

## Step 0 — Configuration Extraction

Extracted from project CLAUDE.md Security Configuration:

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Component label pattern**: pscomponent:
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa

---

## Query 1: Untriaged Issues

**JQL query constructed from Security Configuration:**

```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

Uses project key `TC` and vulnerability issue type ID `10024` from the Security Configuration.

**Results (4 issues):**

### Status: New

| # | Issue | Status | CVE | Summary | Created |
|---|-------|--------|-----|---------|---------|
| 1 | TC-9001 | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| 2 | TC-9002 | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| 3 | TC-9004 | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |

**Status-aware handling**: TC-9001, TC-9002, and TC-9004 are in **New** status — proceed with full triage.

### Status: In Progress

| # | Issue | Status | CVE | Summary | Created |
|---|-------|--------|-----|---------|---------|
| 4 | TC-9003 | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |

**Status-aware handling**: TC-9003 is already **In Progress**. This issue may be actively worked on. If selected for triage, the user will be asked whether to proceed or skip.

---

## Query 2: Triaged but still New

**JQL query constructed from Security Configuration:**

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

Uses project key `TC` and vulnerability issue type ID `10024` from the Security Configuration.

**Results (1 issue):**

| # | Issue | Status | CVE | Summary | Created |
|---|-------|--------|-----|---------|---------|
| 1 | TC-9010 | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

These issues were triaged (labeled `ai-cve-triaged`) but remain in **New** status. They may need follow-up or re-triage — the triage output may not have been actioned.

---

## Query 3: Ready for QA Candidates

**JQL query constructed from Security Configuration:**

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

Uses project key `TC` and vulnerability issue type ID `10024` from the Security Configuration. This query finds triaged CVEs still in a pre-QA state — candidates for ON_QA transition once all linked remediation Tasks are complete.

**Results (3 issues):**

For each result, the skill checks `issuelinks` for linked Tasks with link type `Depend` and fetches each linked Task's status to determine whether all remediation work is complete.

### Ready for QA

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

All linked remediation Tasks for TC-9020 are completed (TC-9021 Done, TC-9022 Closed). Consider transitioning TC-9020 to **ON_QA**.

### Excluded from Ready for QA

| Issue | Status | CVE | Summary | Created | Reason |
|-------|--------|-----|---------|---------|--------|
| TC-9023 | In Progress | CVE-2026-39102 | rustls - Certificate validation bypass [rhtpa-2.1] | 2026-05-10 | TC-9025 still In Progress — remediation is not complete |
| TC-9026 | Modified | CVE-2026-39330 | openssl - Buffer overflow in X.509 parsing [rhtpa-2.2] | 2026-05-05 | No linked Tasks with type Depend — no remediation to verify |
