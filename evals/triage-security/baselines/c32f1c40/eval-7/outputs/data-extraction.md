# Step 0 -- Validate Project Configuration

Configuration extracted from CLAUDE.md:

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345
- **Deployment Context**: not present in Source Repositories table -- defaulting all repositories to `upstream`

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories

| Repository | URL | Local Path | Deployment Context |
|------------|-----|------------|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | upstream (default) |

---

# Step 0.8 -- Assign and Transition to Assigned

**Proposed actions** (not executed -- eval mode):

1. Retrieve current user's Jira account ID via `jira.user_info()`
2. Assign TC-8006 to the current user via `jira.edit_issue(TC-8006, assignee=<current-user-account-id>)`
3. Discover available transitions via `jira.get_transitions(TC-8006)`
4. Transition TC-8006 from New to Assigned (select the transition whose target status name is "Assigned")

These actions provide immediate visibility into who is actively triaging TC-8006 and enable Step 7 (Concurrent Triage Detection).

---

# Step 1 -- Data Extraction

**Issue**: TC-8006

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.1] |
| Issue Type | Vulnerability |
| Status | New |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.1 (from summary suffix `[rhtpa-2.1]`) |
| Affects Versions (Jira field) | RHTPA 2.1.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Due date | 2026-07-15 |
| Upstream fix PR | (none in remote links) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Existing comments | None |

### Stream scope resolution

The issue summary contains the stream suffix `[rhtpa-2.1]`, which maps to the **2.1.x** stream in the Version Streams table. Triage is scoped to the 2.1.x stream only.

### Ecosystem detection

The vulnerable library is **quinn-proto**, a Rust crate. Based on the Ecosystem Mappings table in the 2.1.x stream's security-matrix.md, this falls under the **Cargo** ecosystem.

- **Category**: Source dependency
- **Remediation tasks per stream**: 2 (upstream backport + downstream propagation)
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`
- **Upstream branch**: `release/0.3.z`

### Deployment context lookup

The affected component `pscomponent:org/rhtpa-server` maps to repository `rhtpa-backend`. The Source Repositories table does not have a Deployment Context column, so the deployment context defaults to `upstream`.

### Existing issue links

TC-8006 has the following pre-existing issue links:

| Link Type | Direction | Linked Issue |
|-----------|-----------|--------------|
| Related | outward (TC-8006 -> TC-8001) | TC-8001 (CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]) |

This pre-existing link is relevant for Step 4 (Sibling Check) -- it will be checked for idempotency before attempting to create a new link.
