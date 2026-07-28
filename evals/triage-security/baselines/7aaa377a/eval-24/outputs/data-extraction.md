# Step 0 — Configuration Validation

## Project Configuration Extracted

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345
- **Upstream Affected Component custom field**: _(not configured)_
- **PS Component custom field**: _(not configured)_
- **Stream custom field**: _(not configured)_
- **ProdSec contact email**: _(not configured)_
- **ProdSec Jira account ID**: _(not configured)_
- **Embargo policy URL**: _(not configured)_

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories — Deployment Context

The Source Repositories table has the following columns: **Repository | URL | Local Path**.

The **Deployment Context column is absent**. Per backward compatibility rules (S1.78), all repositories default to `upstream` deployment context.

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | upstream _(default — no Deployment Context column in Source Repositories table)_ |

## Step 0.3 — Matrix Staleness Check

Security matrix Last-Updated timestamp: `2026-06-28T10:00:00Z`
Current date: 2026-07-28
Days since last update: 30 days

The matrix is older than the 14-day threshold, but for this eval, external tools are not invoked. Proceeding with the current matrix data as provided.

## Step 0.7 — Early Assignment (proposed actions)

Before extracting CVE data, the following actions would be performed:

1. **Assign TC-8001 to current user**: `jira.edit_issue(TC-8001, assignee=<current-user-account-id>)`
2. **Discover transitions**: `jira.get_transitions(TC-8001)` — select transition whose target status is "Assigned"
3. **Transition to Assigned**: `jira.transition_issue(TC-8001, <assigned-transition-id>)` (issue is currently in New status)

---

# Step 1 — Data Extraction

## Parsed CVE Data Table

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |

### Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams table. Triage is scoped to this stream.

### Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, the ecosystem is **Cargo**.

Cargo is a **source dependency ecosystem** per the classification table. This means remediation will produce **two tasks** per stream: upstream backport + downstream propagation.

### Deployment Context Lookup

The affected repository identified from the component label `pscomponent:org/rhtpa-server` is **rhtpa-backend**. The deployment context for rhtpa-backend was looked up from the Source Repositories mapping extracted in Step 0.

- **Repository**: rhtpa-backend
- **Deployment context**: `upstream` (defaulted — the Source Repositories table has no Deployment Context column)

This deployment context value is recorded as part of the CVE metadata. Since the deployment context is the default `upstream` and was assigned due to the absence of the Deployment Context column (backward compatibility), no Coordination Guidance subsection will be included in remediation task descriptions.
