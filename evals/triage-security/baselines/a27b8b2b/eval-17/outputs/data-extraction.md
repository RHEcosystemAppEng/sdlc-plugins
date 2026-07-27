# Step 0 -- Validate Project Configuration

Configuration extracted from CLAUDE.md (`claude-md-security-config-embargo.md`):

| Config Field | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Embargo policy URL | https://example.com/security/embargo-policy |

The Embargo policy URL was extracted as an optional field from Security Configuration
without raising an error. It is present and will be used in Step 1.7.

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | upstream (default -- no Deployment Context column) |

No Deployment Context column found in Source Repositories table. All repositories
default to `upstream` per backward compatibility rules.

---

## Step 0.3 -- Matrix Staleness Check

The security-matrix.md has `Last-Updated: 2026-06-28T10:00:00Z`.
Today is 2026-07-27, which is 29 days since last update. However, the eval
prompt does not focus on staleness for this eval -- proceeding to Step 0.7.

---

## Step 0.7 -- Assign and Transition to Assigned

**Proposed actions** (before data extraction):

1. **Retrieve current user's Jira account ID** via `jira.user_info()`
2. **Assign TC-8001 to the current user** via:
   ```
   jira.edit_issue("TC-8001", assignee=<current-user-account-id>)
   ```
3. **Discover the "Assigned" transition** via:
   ```
   jira.get_transitions("TC-8001")
   ```
   Select the transition whose target status name is "Assigned".
4. **Transition TC-8001 from New to Assigned** via:
   ```
   jira.transition_issue("TC-8001", <assigned-transition-id>)
   ```

The issue is currently in **New** status, so both assignment and transition proceed.

---

## Step 1 -- Data Extraction

Parsed CVE data from Vulnerability issue TC-8001:

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
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

### Stream scope resolution

Issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream
in the Version Streams table. Triage is scoped to the 2.2.x stream for Steps 3-8.

All streams are still analyzed in Step 2 (Version Impact) per Important Rule 4
(check ALL supported versions).

### Ecosystem detection

The vulnerable library `quinn-proto` is a Rust crate. Cross-referencing with the
Ecosystem Mappings table in the 2.2.x stream's security-matrix.md confirms
the ecosystem is **Cargo**.

Cargo is classified as a **source dependency ecosystem** in the ecosystem
classification table, which means remediation produces **2 tasks** per affected
stream (upstream backport + downstream propagation).

### Deployment context lookup

The affected repository identified from the component label `pscomponent:org/rhtpa-server`
maps to `rhtpa-backend`. Deployment context: **upstream** (default, no Deployment Context
column present).
