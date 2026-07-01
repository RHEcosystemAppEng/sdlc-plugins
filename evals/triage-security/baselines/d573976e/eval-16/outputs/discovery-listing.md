# Discovery Mode — Untriaged Vulnerability Issues

## Step 0 — Validate Project Configuration

Configuration extracted from CLAUDE.md:

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345

## Step 0.5 — JIRA Access Initialization

JIRA access initialized (mock — no actual connection in eval mode).

---

## Query 1: Untriaged Issues

**JQL:**
```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

### New (3 issues)

| # | Issue | Status | CVE ID | Summary | Created |
|---|-------|--------|--------|---------|---------|
| 1 | TC-9001 | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| 2 | TC-9002 | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| 3 | TC-9004 | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |

**Status-aware handling:** These issues are in **New** status — ready for full triage. Select an issue number to begin triage.

### In Progress (1 issue)

| # | Issue | Status | CVE ID | Summary | Created |
|---|-------|--------|--------|---------|---------|
| 4 | TC-9003 | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |

**Status-aware handling:** TC-9003 is already **In Progress**. It may be actively worked on. Options:
1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
2. Skip this issue

---

## Query 2: Triaged but still New

**JQL:**
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

**Results** (1 issue):

| # | Issue | Status | CVE ID | Summary | Created |
|---|-------|--------|--------|---------|---------|
| 1 | TC-9010 | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

This issue was triaged (has `ai-cve-triaged` label) but remains in **New** status. It may need follow-up or re-triage — the triage completed but the issue was never actioned.

---

## Query 3: Ready for QA

**JQL:**
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

This query returned 3 candidate issues. Each candidate's linked remediation Tasks (link type "Depend") were inspected to determine whether all remediation is complete.

### Qualified for Ready for QA (1 issue)

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

All linked remediation Tasks for TC-9020 are completed (TC-9021: Done, TC-9022: Closed). Consider transitioning TC-9020 to **ON_QA**.

### Excluded from Ready for QA (2 issues)

| Issue | Status | CVE | Summary | Created | Reason |
|-------|--------|-----|---------|---------|--------|
| TC-9023 | In Progress | CVE-2026-39102 | rustls - Certificate validation bypass [rhtpa-2.1] | 2026-05-10 | TC-9025 still In Progress — remediation not complete |
| TC-9026 | Modified | CVE-2026-39330 | openssl - Buffer overflow in X.509 parsing [rhtpa-2.2] | 2026-05-05 | No linked Tasks with type "Depend" — no remediation to verify |

---

Select an issue key to begin triage, or choose a Ready for QA issue to transition.
