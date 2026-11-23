# triage-security — Discovery Mode Listing

Invoked without an issue key, so the skill runs in **discovery mode** (interactive mode; `FULLSEND_OUTPUT_DIR` is not set).

## Step 0 — Configuration extracted (from CLAUDE.md Security Configuration)

| Setting | Value |
|---|---|
| Project key | `TC` |
| Cloud ID | `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| Vulnerability issue type ID | `10024` |
| Jira version prefix | `RHTPA` |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | `customfield_12345` |
| Version Streams | `2.1.x` (rhtpa-release.0.3.z), `2.2.x` (rhtpa-release.0.4.z) |
| Source Repositories | `rhtpa-backend` (no Deployment Context column, so it defaults to `upstream`) |

The required configuration is all present (Repository Registry, Jira Configuration, Code Intelligence, and Security Configuration with Product Lifecycle, Version Streams and Source Repositories). Discovery continues.

## JQL queries constructed

The queries below fill in `<project-key>` = `TC` and `<vulnerability-issue-type-id>` = `10024` from the Security Configuration.

**Query 1: Untriaged** (fields: summary, labels, status, created; maxResults: 20)
```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

**Query 2: Triaged but still New** (fields: summary, labels, status, created; maxResults: 10)
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

**Query 3: Ready for QA candidates** (fields: summary, labels, status, created, issuelinks; maxResults: 20)
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

**Query 4: Release Jira summary** (fields: summary, status, issuelinks, parent; maxResults: 10)
```
project = TC AND issuetype = Task AND summary ~ 'RHTPA' AND summary ~ 'CVE triage' ORDER BY created DESC
```

The constructed Queries 1 to 3 match the JQL recorded in the mock search results exactly.

---

## 1. Untriaged (4 issues)

### Status: New (3)

| # | Issue | Status | CVE | Summary | Created |
|---|---|---|---|---|---|
| 1 | TC-9001 | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| 2 | TC-9002 | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| 3 | TC-9004 | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |

### Status: In Progress (1)

| # | Issue | Status | CVE | Summary | Created |
|---|---|---|---|---|---|
| 4 | TC-9003 | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |

> WARNING: TC-9003 is already **In Progress** and may be actively worked on. If you select it, you will be asked to confirm before triage starts.

## 2. Triaged but still New (1 issue) — FLAGGED

These issues carry the `ai-cve-triaged` label but are still in **New**. They were triaged but nobody moved them forward, so they may need follow-up or re-triage.

### Status: New (1)

| # | Issue | Status | CVE | Summary | Created |
|---|---|---|---|---|---|
| 5 | TC-9010 | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

## 3. Ready for QA (1 issue)

These are triaged CVEs where every linked "Depend" remediation Task is Done or Closed.

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|---|---|---|---|---|---|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

- **TC-9020**: Consider transitioning to ON_QA.

Candidates from Query 3 that were excluded:

| Issue | Status | CVE | Reason excluded |
|---|---|---|---|
| TC-9023 | In Progress | CVE-2026-39102 (rustls) | Linked Task TC-9025 is still In Progress, so remediation is not finished (TC-9024 is Done) |
| TC-9026 | Modified | CVE-2026-39330 (openssl) | Has no linked Tasks with link type "Depend", so there is no remediation to verify |

## 4. Release Jira Summary

The mock data set contains no results for Query 4, so there are no release Epic or Task rows to show.

| Release Epic | Release Task | CVEs Tracked | Remediation Done | Remediation Pending |
|---|---|---|---|---|
| (no data provided) | — | — | — | — |

---

Select an issue number (1 to 5) to start triage, or enter an issue key.
