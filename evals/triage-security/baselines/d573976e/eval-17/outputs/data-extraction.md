# Step 0 -- Validate Project Configuration

Configuration extracted from CLAUDE.md (`claude-md-security-config-embargo.md`):

| Setting | Value |
|---------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Embargo policy URL | https://example.com/security/embargo-policy |
| ProdSec contact email | _(not configured)_ |
| ProdSec Jira account ID | _(not configured)_ |
| Upstream Affected Component custom field | _(not configured)_ |
| PS Component custom field | _(not configured)_ |
| Stream custom field | _(not configured)_ |

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories

| Repository | URL | Local Path | Deployment Context |
|------------|-----|------------|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | _(column absent -- default: upstream)_ |

**Note**: The Source Repositories table does NOT have a Deployment Context column. Per backward compatibility rules, all repositories default to `upstream` and no Coordination Guidance subsection will be included in remediation task descriptions.

All required sections (Repository Registry, Jira Configuration, Code Intelligence, Security Configuration with Product Lifecycle, Version Streams, and Source Repositories) are present. Configuration is valid.

---

# Step 0.3 -- Matrix Staleness Check

Reading security-matrix.md for each configured version stream:

- **Stream 2.1.x** and **Stream 2.2.x**: Both are covered in the combined `security-matrix-mock.md` file.
- **Last-Updated timestamp**: `2026-06-28T10:00:00Z`
- **Current date**: 2026-07-01
- **Days since last update**: 3 days
- **Threshold**: 14 days

The matrix was last updated 3 days ago, which is within the 14-day staleness threshold. No warning is needed. Proceeding silently to Step 0.5.

---

# Step 1 -- Data Extraction

## Parsed CVE Data from TC-8001

| Field | Value |
|-------|-------|
| Issue Key | TC-8001 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| CVE ID | CVE-2026-31812 (from labels and summary) |
| Affected component | pscomponent:org/rhtpa-server (from labels) |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
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
| Reporter | _(not specified in fixture -- would be extracted from Jira API response)_ |

### Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`. Mapping to configured Version Streams:
- `rhtpa-2.2` maps to stream **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`)

**Issue stream scope**: 2.2.x

Steps 3 and 4 will be scoped to the 2.2.x stream. Versions from other streams (2.1.x) are analyzed for cross-stream impact (Step 8 Case B) but do not affect Affects Versions correction for this issue.

### Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. The Ecosystem Mappings table in the 2.2.x stream's security-matrix.md lists:
- **Cargo** -- Repository: backend, Lock File: `Cargo.lock`, Check Command: `git show <tag>:Cargo.lock`, Upstream Branch: `release/0.4.z`
- **RPM** -- Repository: --, Lock File: `rpms.lock.yaml`, Check Command: `git show <tag>:rpms.lock.yaml`, Upstream Branch: --

quinn-proto is a Rust crate, which falls under the **Cargo** ecosystem. This is a supported ecosystem listed in the Ecosystem Mappings table.

**Detected ecosystem**: Cargo

### Deployment Context Lookup

The affected repository is identified from the component label `pscomponent:org/rhtpa-server`, which maps to `rhtpa-backend` in the Source Repositories table. The Source Repositories table does NOT have a Deployment Context column. Per backward compatibility rules, the deployment context defaults to `upstream`. However, since no Deployment Context column exists, no Coordination Guidance subsection will be added to remediation task descriptions.

**Deployment context**: upstream (default -- column absent)
