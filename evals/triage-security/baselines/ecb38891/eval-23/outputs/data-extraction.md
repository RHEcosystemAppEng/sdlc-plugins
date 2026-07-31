# Step 0 -- Validate Project Configuration

## Configuration Extracted

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories (with Deployment Context)

The Source Repositories table includes a **Deployment Context** column. Each repository's deployment context is parsed:

| Repository | URL | Local Path | Deployment Context |
|------------|-----|------------|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | customer-shipped |

Step 0 successfully extracted the Deployment Context column from the Source Repositories table and parsed rhtpa-backend as **customer-shipped**.

---

# Step 0.7 -- Assign and Transition to Assigned

Before extracting CVE data, assign the issue and transition it to Assigned status:

1. **Retrieve current user's Jira account ID:**
   - Proposed action: `jira.user_info()` to get the current user's account ID.

2. **Assign TC-8001 to the current user:**
   - Proposed action: `jira.edit_issue("TC-8001", assignee=<current-user-account-id>)`

3. **Discover the Assigned transition:**
   - Proposed action: `jira.get_transitions("TC-8001")` to find the transition whose target status name is "Assigned".

4. **Transition TC-8001 to Assigned:**
   - TC-8001 is currently in **New** status, so the transition to Assigned proceeds.
   - Proposed action: `jira.transition_issue("TC-8001", <assigned-transition-id>)`

---

# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x (scoped -- matches configured Version Stream 2.2.x) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Ecosystem | Cargo (quinn-proto is a Rust crate) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |

### Deployment Context Lookup

The affected component label `pscomponent:org/rhtpa-server` maps to repository **rhtpa-backend** (the backend source repository in the Ecosystem Mappings table). Looking up the deployment context from the Source Repositories mapping:

- **Repository**: rhtpa-backend
- **Deployment Context**: **customer-shipped**

This deployment context is recorded as part of the CVE metadata and will be used in Step 8 (Remediation) when generating coordination guidance in remediation task descriptions.

### Ecosystem Classification

- **Ecosystem**: Cargo (source dependency)
- **Category**: Source dependency
- **Remediation tasks per stream**: 2 (upstream backport + downstream propagation)

The Cargo ecosystem is listed in the 2.2.x stream's Ecosystem Mappings table with:
- Repository: backend
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`
