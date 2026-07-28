# Step 0 -- Validate Project Configuration

Configuration extracted from CLAUDE.md:

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345
- **Embargo policy URL** _(optional)_: https://example.com/security/embargo-policy
- **ProdSec contact email**: _(not configured -- skipped silently)_
- **ProdSec Jira account ID**: _(not configured -- skipped silently)_
- **Upstream Affected Component custom field**: _(not configured -- Step 4.3 skipped)_
- **PS Component custom field**: _(not configured)_
- **Stream custom field**: _(not configured)_

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | upstream _(default -- no Deployment Context column)_ |

The Deployment Context column is absent from the Source Repositories table. All repositories default to `upstream` (backward compatibility). Coordination Guidance subsections will be omitted from remediation task descriptions.

## Step 0.3 -- Matrix Staleness Check

Security matrix Last-Updated timestamp: 2026-06-28T10:00:00Z
Current date: 2026-07-28
Days since last update: 30 days

The matrix is older than the 14-day default threshold. In a live triage, a staleness warning would be presented with three options (Refresh now, Proceed anyway, Stop). For this eval, we assume the engineer chose "Proceed anyway."

## Step 0.7 -- Assign and Transition to Assigned

Proposed actions (not executed -- eval mode):

1. Retrieve current user's Jira account ID via `jira.user_info()`
2. Assign TC-8001 to the current user via `jira.edit_issue(TC-8001, assignee=<current-user-account-id>)`
3. Discover the "Assigned" transition via `jira.get_transitions(TC-8001)` -- select the transition whose target status name is "Assigned"
4. Transition TC-8001 to Assigned via `jira.transition_issue(TC-8001, <assigned-transition-id>)` (issue is currently in New status)

# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |
| Reporter | _(from Jira issue reporter field)_ |

### Stream scope resolution

Issue summary contains stream suffix `[rhtpa-2.2]`:
- Parsed suffix: rhtpa-2.2 maps to stream **2.2.x**
- Matched to Version Streams table: 2.2.x stream (rhtpa-release.0.4.z)
- Issue stream scope: **2.2.x** (scoped)

### Ecosystem detection

Library: quinn-proto
Context: Rust crate (QUIC transport library)
Ecosystem: **Cargo** (source dependency ecosystem)
Remediation task count per stream: **2** (upstream backport + downstream propagation)

### Deployment context lookup

Affected repository from component label `pscomponent:org/rhtpa-server`: rhtpa-backend
Deployment context: **upstream** (default -- no Deployment Context column in Source Repositories table)
