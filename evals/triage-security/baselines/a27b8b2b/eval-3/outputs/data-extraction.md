# Step 0 -- Validate Project Configuration

Configuration extracted from CLAUDE.md:

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345

Version Streams:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

Source Repositories (no Deployment Context column -- defaulting all to `upstream`):

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | upstream (default) |

## Step 0.7 -- Assign and Transition to Assigned

Before extracting CVE data, the following early assignment actions are proposed:

1. **Retrieve current user's Jira account ID** via `jira.user_info()`
2. **Assign TC-8003 to the current user** via `jira.edit_issue(TC-8003, assignee=<current-user-account-id>)`
3. **Discover the Assigned transition** via `jira.get_transitions(TC-8003)` -- select the transition whose target status name is "Assigned"
4. **Transition TC-8003 to Assigned** via `jira.transition_issue(TC-8003, <assigned-transition-id>)` -- the issue is currently in New status, so this transition is applicable

These actions provide immediate visibility into who is actively triaging the issue and enable Step 7 (Concurrent Triage Detection) to reliably identify active work.

# Step 1 -- Data Extraction

Fetched issue TC-8003 from Jira. Parsed fields:

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | (none in remote links) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | (none) |

### Stream scope resolution

The issue summary contains stream suffix `[rhtpa-2.2]`. Mapped to configured Version Stream **2.2.x**. Triage is scoped to the 2.2.x stream only.

### Ecosystem detection

The vulnerable library is **quinn-proto**, a Rust crate. Based on the library name and the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, the ecosystem is classified as **Cargo** (source dependency ecosystem). This means remediation would produce two tasks per stream (upstream backport + downstream propagation) -- however, this determination is relevant only if triage proceeds past the duplicate check in Step 4.
