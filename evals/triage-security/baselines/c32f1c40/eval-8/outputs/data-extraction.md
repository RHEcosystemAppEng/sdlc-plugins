# Step 0 -- Validate Project Configuration

Configuration extracted from CLAUDE.md:

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345
- **Upstream Affected Component custom field**: customfield_10632
- **PS Component custom field**: customfield_10669
- **Stream custom field**: customfield_10832
- **Deployment Context**: not configured (column absent from Source Repositories table; defaulting all repositories to upstream)

Version Streams:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

Source Repositories:

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | upstream (default) |

# Step 0.8 -- Assign and Transition to Assigned

**Proposed actions** (not executed -- eval prohibits Jira calls):

1. Retrieve current user's Jira account ID via `jira.user_info()`
2. Assign TC-8010 to the current user via `jira.edit_issue(TC-8010, assignee=<current-user-account-id>)`
3. Discover available transitions via `jira.get_transitions(TC-8010)` and select the transition whose target status is "Assigned"
4. Transition TC-8010 from New to Assigned status (issue is currently in New status, so the transition proceeds)

# Step 1 -- Data Extraction

**Issue**: TC-8010

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-44492 |
| Affected component | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | axios |
| Affected version range | versions before 1.8.2 (< 1.8.2) |
| Fixed version | 1.8.2 |
| CVSS | 8.1 (High) |
| Upstream fix PR | _(not provided in remote links)_ |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 |
| Due date | 2026-08-01 |
| Existing comments | None |
| Reporter | _(from issue data)_ |
| Upstream Affected Component (customfield_10632) | axios |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-ui |
| Stream (customfield_10832) | rhtpa-2.2 |

### Stream scope resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams table. Triage is scoped to the 2.2.x stream only.

### Ecosystem detection

The vulnerable library is **axios**, which is an npm package (JavaScript/TypeScript). The ecosystem is **npm**.

Note: The security-matrix.md for the 2.2.x stream includes Ecosystem Mappings for Cargo and RPM but does not include an npm ecosystem mapping. The npm ecosystem detection is based on the library name and component context (axios is a well-known npm package used in rhtpa-ui, a frontend/UI component).

### Deployment context lookup

The affected component is pscomponent:org/rhtpa-ui. The Source Repositories table does not include a Deployment Context column (backward compatibility), so the deployment context defaults to **upstream** for all repositories.
