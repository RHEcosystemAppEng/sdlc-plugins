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
- **Deployment Context**: absent from Source Repositories table -- defaulting all repositories to `upstream`

Version Streams:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

Source Repositories:

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | upstream (default) |

---

# Step 0.8 -- Assign and Transition to Assigned

**Proposed actions** (not executed -- eval prohibits external tool calls):

1. Retrieve the current user's Jira account ID via `jira.user_info()`
2. Assign TC-8011 to the current user via `jira.edit_issue(TC-8011, assignee=<current-user-account-id>)`
3. Discover transitions via `jira.get_transitions(TC-8011)` and select the transition whose target status is "Assigned"
4. Transition TC-8011 from New to Assigned (issue is currently in New status)

---

# Step 1 -- Data Extraction

Parsed CVE data from Vulnerability issue TC-8011:

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-45678 |
| Affected component | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | webpack |
| Affected version range | versions before 5.98.0 (< 5.98.0) |
| Fixed version | 5.98.0 |
| CVSS | 7.8 (High) |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 |
| Due date | 2026-08-15 |
| Upstream Affected Component (customfield_10632) | webpack |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-ui |
| Stream (customfield_10832) | rhtpa-2.2 |
| Existing comments | None |
| Existing issue links | None |

### Stream scope resolution

Issue summary contains stream suffix `[rhtpa-2.2]` which maps to the **2.2.x** stream in the Version Streams table. Triage is scoped to the 2.2.x stream only.

### Ecosystem detection

The vulnerable library is **webpack**, which is a JavaScript/TypeScript build tool distributed via npm. The detected ecosystem is **npm**.

Note: The security-matrix.md Ecosystem Mappings table for the 2.2.x stream lists Cargo and RPM ecosystems but does not include npm. The npm ecosystem is not present in the configured Ecosystem Mappings. However, the cross-CVE overlap check (Step 4.3) can still proceed based on the Upstream Affected Component field, since it operates on component-level matching rather than ecosystem-specific lock file analysis.

### Deployment context lookup

The affected component is pscomponent:org/rhtpa-ui. The Source Repositories table does not include a Deployment Context column, so all repositories default to `upstream`.
