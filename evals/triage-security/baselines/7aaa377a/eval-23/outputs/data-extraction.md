# Step 0 -- Validate Project Configuration

## Configuration Extraction

| Field | Value |
|-------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories (with Deployment Context)

The Source Repositories table includes a **Deployment Context** column. Each repository is parsed into a mapping of repository name to deployment context.

| Repository | URL | Local Path | Deployment Context |
|------------|-----|------------|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | customer-shipped |

Parsed mapping: `rhtpa-backend` -> `{ url: "https://github.com/rhtpa/rhtpa-backend", deployment_context: "customer-shipped" }`

---

# Step 0.7 -- Assign and Transition to Assigned

**Proposed actions** (require confirmation before execution):

1. **Retrieve current user's Jira account ID** via `jira.user_info()`
2. **Assign TC-8001** to the current user via `jira.edit_issue(TC-8001, assignee=<current-user-account-id>)`
3. **Discover the Assigned transition** via `jira.get_transitions(TC-8001)` -- select the transition whose target status name is "Assigned"
4. **Transition TC-8001 to Assigned** via `jira.transition_issue(TC-8001, <assigned-transition-id>)` -- the issue is currently in New status, so the transition proceeds

---

# Step 1 -- Data Extraction

## Parsed CVE Data Table

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

### Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream from the Version Streams table. Triage is scoped to the 2.2.x stream. The 2.1.x stream will be checked for cross-stream impact in Step 8 Case A.

### Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. Looking at the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, the **Cargo** ecosystem is configured with:
- Repository: backend
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`

Cargo is a **source dependency** ecosystem per the classification table, which means remediation produces **two tasks** per stream: upstream backport + downstream propagation.

### Deployment Context Lookup

The affected component label is `pscomponent:org/rhtpa-server`. The associated repository from the Source Repositories table is **rhtpa-backend**.

Deployment context for `rhtpa-backend`: **customer-shipped**

This deployment context is recorded as part of the CVE metadata and will be used in Step 8 to generate coordination guidance in remediation task descriptions.
