# Step 0.8 -- Early Assignment

**Proposed actions (not executed -- eval prohibits Jira calls):**

1. Assign TC-8021 to the current user.
2. Retrieve available transitions via `jira.get_transitions(TC-8021)`.
3. Select the transition whose target status name is "Assigned".
4. Transition TC-8021 from New to Assigned (issue is currently in New status).

These actions provide immediate visibility into who is actively triaging the issue and enable Step 7 (Concurrent Triage Detection) to identify active work.

---

# Step 0 -- Configuration Validation

Extracted from project CLAUDE.md:

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345
- **Upstream Affected Component custom field**: customfield_10632 (assumed configured per eval prompt)
- **Deployment Context**: Source Repositories table does not have a Deployment Context column; defaulting all repositories to `upstream`.

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

# Step 1 -- Data Extraction

**Issue**: TC-8021
**Source fixture**: vuln-issue-standard.md (data applied to TC-8021 per eval prompt)

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x (scoped -- suffix [rhtpa-2.2] maps to the 2.2.x stream) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Ecosystem | **Cargo** (Rust crate -- quinn-proto is a Cargo dependency in the backend repository) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Upstream Affected Component (customfield_10632) | quinn-proto |
| Existing comments | None |

### Stream scope resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams table. Triage is scoped to this stream only. However, version impact analysis will still check all supported versions per Important Rule 4, and cross-stream impact will be assessed in Case A.

### Ecosystem detection

The vulnerable library `quinn-proto` is a Rust crate. The Ecosystem Mappings table in the 2.2.x stream's security-matrix.md lists **Cargo** as a supported ecosystem with:
- Repository: backend
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`

Cargo is a **source dependency ecosystem**, which means remediation produces two tasks per stream: upstream backport (or dependency bump) + downstream propagation.

### Deployment context lookup

The affected repository `rhtpa-backend` is found in the Source Repositories table. Since the Deployment Context column is absent from the Source Repositories table, the deployment context defaults to `upstream`. No Coordination Guidance subsection will be included in remediation task descriptions (backward compatibility).
