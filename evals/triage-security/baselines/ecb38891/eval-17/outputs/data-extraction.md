# Step 0 -- Validate Project Configuration

Configuration extracted from CLAUDE.md:

| Config Field | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Embargo policy URL *(optional)* | https://example.com/security/embargo-policy |

**Embargo policy URL** was extracted as an optional field from Security Configuration
without raising an error. This field is backward compatible -- when absent, Step 1.7
is skipped entirely. Since it is present in this configuration, Step 1.7 will
evaluate the CVE severity against the embargo threshold after data extraction.

**Version Streams:**

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

**Source Repositories:**

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | upstream *(default -- no Deployment Context column)* |

No Deployment Context column found in Source Repositories table. All repositories
default to `upstream` (backward compatibility).

---

# Step 0.7 -- Assign and Transition to Assigned

Before data extraction, the following early assignment actions are performed:

1. **Retrieve current user's Jira account ID:**
   ```
   jira.user_info()
   ```
   Result: current user account ID retrieved.

2. **Assign the issue to the current user:**
   ```
   jira.edit_issue("TC-8001", assignee=<current-user-account-id>)
   ```
   Proposed action: Assign TC-8001 to current user.

3. **Discover the target transition dynamically:**
   ```
   jira.get_transitions("TC-8001")
   ```
   Select the transition whose target status name is "Assigned". The transition ID
   is discovered at runtime -- not hardcoded.

4. **Transition to Assigned (issue is currently in New status):**
   ```
   jira.transition_issue("TC-8001", <assigned-transition-id>)
   ```
   Proposed action: Transition TC-8001 from New to Assigned status.

These actions provide immediate visibility into who is actively triaging the issue
and enable Step 7 (Concurrent Triage Detection) to reliably identify active work.

---

# Step 1 -- Data Extraction

**Parsed CVE Data Table:**

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] (from summary suffix) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 (versions before 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |

**Stream scope resolution:**

- Summary suffix: `[rhtpa-2.2]`
- Mapped to Version Streams: **2.2.x** stream
- Issue stream scope: **scoped to 2.2.x**

**Ecosystem detection:**

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo** (source dependency)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Remediation task structure: **2 tasks per stream** (upstream backport + downstream propagation)

**Deployment context lookup:**

- Affected repository (from component label pscomponent:org/rhtpa-server): rhtpa-backend
- Deployment context: **upstream** (default -- no Deployment Context column in Source Repositories table)
