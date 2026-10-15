# Step 0 -- Validate Project Configuration

Configuration extracted from CLAUDE.md:

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345
- **Upstream Affected Component custom field**: not configured (Step 4.3 and Step 7 will be skipped)
- **ProdSec contact**: not configured (skip @mentions silently)
- **Embargo policy URL**: not configured (Step 1.7 skipped)
- **Deployment Context column**: absent from Source Repositories table -- defaulting all repositories to `upstream` (backward compatibility per Important Rule; coordination guidance will be omitted from remediation tasks)

**Version Streams**:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

**Source Repositories**:

| Repository | URL | Local Path | Deployment Context |
|------------|-----|------------|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | upstream (default) |

## Step 0.8 -- Assign and Transition to Assigned

**Proposed actions** (not executed -- eval mode):

1. Retrieve current user's Jira account ID via `jira.user_info()`
2. Assign TC-8050 to current user via `jira.edit_issue(TC-8050, assignee=<current-user-account-id>)`
3. Discover transitions via `jira.get_transitions(TC-8050)` and select the transition whose target status is "Assigned"
4. Transition TC-8050 from New to Assigned (issue is currently in New status, so transition proceeds)

---

# Step 1 -- Data Extraction

Parsed CVE data from Vulnerability issue TC-8050:

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99001 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | criterion |
| Affected version range | < 0.5.2 |
| Fixed version | 0.5.2 |
| CVSS | 5.3 (Medium) |
| Upstream fix PR | (none in remote links) |
| Advisory URL | (none in remote links) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99001 |
| Due date | 2026-08-01 |
| Existing comments | (none) |

### Stream scope resolution

Issue summary contains stream suffix `[rhtpa-2.2]`. Mapping:
- `[rhtpa-2.2]` maps to stream **2.2.x** in the Version Streams table
- **Issue stream scope**: 2.2.x -- triage is scoped to this stream only

### Ecosystem detection

The vulnerable library is **criterion**, a Rust crate. Based on the library name and the component context (pscomponent:org/rhtpa-server pointing to rhtpa-backend which uses rust-analyzer), the ecosystem is **Cargo**.

Cargo is listed in the 2.2.x stream's Ecosystem Mappings table:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

Ecosystem classification: **Source dependency** -- Cargo produces 2 tasks per stream (upstream backport + downstream propagation).

### Deployment context lookup

Affected repository: rhtpa-backend. The Source Repositories table does not include a Deployment Context column, so all repositories default to `upstream`. Coordination guidance will be omitted from remediation task descriptions (backward compatibility).
