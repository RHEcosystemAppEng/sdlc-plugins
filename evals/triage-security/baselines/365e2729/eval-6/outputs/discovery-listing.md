# triage-security — Discovery Mode Listing

Invoked without an issue key, so the skill runs in **discovery mode**.

## Step 0 – Configuration Validation

Mode: **interactive** (`FULLSEND_OUTPUT_DIR` is not set, so Steps 0.6 and 0.7 make no changes).

| Required section | Status | Extracted values |
|---|---|---|
| Repository Registry | Present (1 entry) | rhtpa-backend |
| Jira Configuration | Present | Project key: `TC`, Cloud ID: `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| Code Intelligence | Present | `mcp__<serena-instance>__<tool>`, instance `serena_backend` |
| Security Configuration → Product Lifecycle | Present | Jira version prefix: `RHTPA`, Vulnerability issue type ID: **`10024`**, Component label pattern: `pscomponent:`, VEX field: `customfield_12345` |
| Security Configuration → Version Streams | Present (2) | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Security Configuration → Source Repositories | Present (1) | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) |

The configuration is complete, so discovery can go ahead.

## Constructed JQL Queries

These queries are built from the Security Configuration: `<project-key>` = `TC`, `<vulnerability-issue-type-id>` = `10024`.

**Query 1 – Untriaged** (maxResults 20, fields: summary, labels, status, created)
```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

**Query 2 – Triaged but still New** (maxResults 10, fields: summary, labels, status, created)
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

**Query 3 – Ready for QA candidates** (maxResults 20, fields: summary, labels, status, created, issuelinks)
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

**Query 4 – Release Jira summary** (maxResults 10, fields: summary, status, issuelinks, parent)
```
project = TC AND issuetype = Task AND summary ~ 'RHTPA' AND summary ~ 'CVE triage' ORDER BY created DESC
```

---

## 1. Untriaged (4 issues)

### Status: New

| # | Issue | Status | CVE | Summary | Created |
|---|---|---|---|---|---|
| 1 | TC-9001 | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| 2 | TC-9002 | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| 3 | TC-9004 | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |

### Status: In Progress

| # | Issue | Status | CVE | Summary | Created |
|---|---|---|---|---|---|
| 4 | TC-9003 | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |

> Warning: TC-9003 is already **In Progress**, so someone may be working on it. If you select it, you will be asked to confirm before triage starts.

## 2. Triaged but still New (1 issue) — FLAGGED

These issues have the `ai-cve-triaged` label but are still in New. They were triaged and then never moved forward, so they may need follow-up or a fresh triage.

### Status: New

| # | Issue | Status | CVE | Summary | Created |
|---|---|---|---|---|---|
| 5 | TC-9010 | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

## 3. Ready for QA (1 issue)

These are triaged CVEs where every linked "Depend" remediation Task is Done or Closed.

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

- **TC-9020**: Consider transitioning to ON_QA.

Excluded from Ready for QA (Query 3 returned them, but the filter removed them):

| Issue | Status | CVE | Reason excluded |
|---|---|---|---|
| TC-9023 | In Progress | CVE-2026-39102 | TC-9025 is still In Progress (TC-9024 is Done), so remediation is not finished |
| TC-9026 | Modified | CVE-2026-39330 | Has no linked Tasks with link type "Depend", so there is no remediation to verify |

## 4. Release Jira Summary

The mock data has no results for Query 4. In a live run, this section would show each `RHTPA <version> CVE triage` release Task with its parent Epic, the number of CVEs tracked (Related links), and how many remediation Tasks are done or pending (Blocks links). No release Jira data is shown here because inventing it would break the "Do NOT fabricate data" rule.

---

Select an issue number (1–5) to triage, or end the session.
