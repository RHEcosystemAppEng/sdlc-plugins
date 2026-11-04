# triage-security — Discovery Mode

Invoked without an issue key. Mode: **interactive** (`FULLSEND_OUTPUT_DIR` not set).

## Step 0 — Configuration validated

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Vulnerability issue type ID | 10024 |
| Jira version prefix | RHTPA |
| Component label pattern | `pscomponent:` |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend |

All required sections are present: Repository Registry, Jira Configuration, Code Intelligence, and Security Configuration (Product Lifecycle, Version Streams, Source Repositories).

---

## 1. Untriaged Vulnerability Issues

JQL: `project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC`

### Status: New

| # | Issue | Status | CVE | Summary | Created |
|---|-------|--------|-----|---------|---------|
| 1 | TC-9001 | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| 2 | TC-9002 | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| 3 | TC-9004 | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |

### Status: In Progress

| # | Issue | Status | CVE | Summary | Created |
|---|-------|--------|-----|---------|---------|
| 4 | TC-9003 | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |

> Note: TC-9003 is already In Progress. If you select it, I will warn that it may be actively worked on and ask whether to proceed or skip.

---

## 2. Triaged but still New (needs follow-up)

JQL: `project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC`

| # | Issue | Status | CVE | Summary | Created |
|---|-------|--------|-----|---------|---------|
| 5 | TC-9010 | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

> **Flagged:** TC-9010 has the `ai-cve-triaged` label but is still in New status. It was triaged but never moved forward and may need follow-up or re-triage.

---

## 3. Ready for QA

JQL: `project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC`

Triaged CVEs where **every** linked remediation Task (link type "Depend") is Done or Closed:

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

- **TC-9020**: Consider transitioning to ON_QA.

Excluded candidates (see `ready-for-qa.md` for details):
- TC-9023: excluded because remediation is still in progress (TC-9025 is In Progress).
- TC-9026: excluded because it has no Depend-linked remediation Tasks, so there is nothing to verify.

---

## 4. Release Jira Summary

JQL: `project = TC AND issuetype = Task AND summary ~ 'RHTPA' AND summary ~ 'CVE triage' ORDER BY created DESC`

No release Task results were provided in the discovery input, so there is no release Jira summary to show. I have not invented any data.

---

**Next step:** Select an issue number (1–5) to start full triage, or pick a Ready for QA issue to review for ON_QA transition. Any Jira mutation, including an ON_QA transition, needs your explicit confirmation first.
