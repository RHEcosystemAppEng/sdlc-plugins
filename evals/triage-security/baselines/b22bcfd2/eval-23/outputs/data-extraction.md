# Step 0 -- Validate Project Configuration

## Configuration Extracted

| Setting | Value |
|---------|-------|
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

The Source Repositories table includes a **Deployment Context** column. Parsed mapping:

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | **customer-shipped** |

The Deployment Context column is present in the Source Repositories table. The repository `rhtpa-backend` is mapped to deployment context `customer-shipped`.

---

## Step 0.3 -- Matrix Staleness Check

The security-matrix.md has `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-07-01. The matrix was last updated 3 days ago, which is within the 14-day default threshold.

**Result**: Matrix is fresh. Proceeding without staleness warning.

---

# Step 1 -- Data Extraction

## Parsed CVE Data Table

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 (versions before 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |
| Status | New |

### Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream from the Version Streams table. The issue is **scoped** to the 2.2.x stream.

### Ecosystem Detection

The vulnerable library is **quinn-proto**, which is a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, this maps to the **Cargo** ecosystem.

Cargo is listed in the Ecosystem Mappings table, so automated triage is supported.

### Deployment Context Lookup

The affected repository is identified from the component label `pscomponent:org/rhtpa-server`, which corresponds to `rhtpa-backend` in the Source Repositories table. Looking up the deployment context:

- **Repository**: rhtpa-backend
- **Deployment Context**: **customer-shipped**

This deployment context is recorded as part of the CVE metadata and will be used in Step 8 (Remediation) to generate coordination guidance in remediation task descriptions.
