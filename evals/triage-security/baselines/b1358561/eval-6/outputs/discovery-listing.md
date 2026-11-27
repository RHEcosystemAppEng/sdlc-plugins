# triage-security — Discovery Mode Listing

Invoked without an issue key, so the skill ran in **discovery mode** (interactive mode;
`FULLSEND_OUTPUT_DIR` was not set).

## Step 0 – Configuration Validation

Everything required is present in `claude-md-security-config.md`:

| Required item | Value | OK |
|---|---|---|
| Repository Registry | rhtpa-backend (serena_backend) | Yes |
| Jira Configuration: Project key | `TC` | Yes |
| Jira Configuration: Cloud ID | `2b9e35e3-6bd3-4cec-b838-f4249ee02432` | Yes |
| Code Intelligence (naming convention) | `mcp__<serena-instance>__<tool>` | Yes |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa | Yes |
| Jira version prefix | `RHTPA` | Yes |
| Vulnerability issue type ID | `10024` | Yes |
| Component label pattern | `pscomponent:` | Yes |
| VEX Justification custom field (optional) | `customfield_12345` | Yes |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) | Yes |
| Source Repositories | rhtpa-backend | Yes |

## JQL Queries Constructed from Security Configuration

The skill templates were filled in with `<project-key>` = `TC`, `<vulnerability-issue-type-id>` = `10024`, and the Jira version prefix `RHTPA`.

**Query 1 — Untriaged issues** (fields: summary, labels, status, created; maxResults: 20)
```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

**Query 2 — Triaged but still New** (fields: summary, labels, status, created; maxResults: 10)
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

**Query 3 — Ready for QA candidates** (fields: summary, labels, status, created, issuelinks; maxResults: 20)
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

**Query 4 — Release Jira summary** (fields: summary, status, issuelinks, parent; maxResults: 10)
```
project = TC AND issuetype = Task AND summary ~ 'RHTPA' AND summary ~ 'CVE triage' ORDER BY created DESC
```

---

## 1. Untriaged (4 issues)

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

Note: TC-9003 is already In Progress, which means someone may be working on it. It has
not been triaged yet (no `ai-cve-triaged` label).

## 2. Triaged but still New (1 issue) — FLAGGED

These issues were triaged but never moved forward. They may need follow-up or re-triage.

| # | Issue | Status | CVE | Summary | Created |
|---|-------|--------|-----|---------|---------|
| 5 | TC-9010 | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

## 3. Ready for QA (1 issue)

Triaged CVEs where every linked "Depend" remediation Task is Done or Closed:

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

- **TC-9020**: Consider transitioning to ON_QA.

Query 3 returned these candidates, which were filtered out:

| Issue | Status | CVE | Reason excluded |
|-------|--------|-----|-----------------|
| TC-9023 | In Progress | CVE-2026-39102 | Linked Task TC-9025 is still In Progress (TC-9024 is Done), so remediation is still underway |
| TC-9026 | Modified | CVE-2026-39330 | It has no linked Tasks of type "Depend", so there is no remediation to verify |

## 4. Release Jira Summary

Query 4 was built (see above), but the eval inputs include no results for it. No
release Epic/Task progress can be reported:

| Release Epic | Release Task | CVEs Tracked | Remediation Done | Remediation Pending |
|-------------|-------------|-------------|-----------------|-------------------|
| (no data provided) | — | — | — | — |

---

Choose an issue number (1–5), or an issue key, to start triage. You can also end the session.
