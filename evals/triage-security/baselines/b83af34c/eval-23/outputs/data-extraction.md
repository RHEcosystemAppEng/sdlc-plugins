# Step 0 -- Validate Project Configuration

## Extracted Configuration

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

Parsed from the Source Repositories table in Security Configuration. The table includes a **Deployment Context** column, so each repository's deployment context is extracted directly.

| Repository | URL | Local Path | Deployment Context |
|------------|-----|------------|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | customer-shipped |

**Deployment context mapping**: rhtpa-backend -> `customer-shipped`

---

# Step 1 -- Data Extraction

## Parsed CVE Data from TC-8001

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |
| CVSS | 7.5 (High) |

## Stream Scope Resolution

The issue summary contains `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams configuration. This issue is scoped to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The 2.2.x stream's Ecosystem Mappings table lists **Cargo** as a supported ecosystem with lock file `Cargo.lock`. Cargo is a source dependency ecosystem, so remediation produces **2 tasks per stream** (upstream backport + downstream propagation).

## Deployment Context Lookup

The affected component label `pscomponent:org/rhtpa-server` identifies the affected repository as **rhtpa-backend**. Looking up the deployment context from the Source Repositories mapping extracted in Step 0:

- **Repository**: rhtpa-backend
- **Deployment context**: **customer-shipped**

This deployment context is recorded as part of the CVE metadata and will be used in Step 8 (Remediation) to generate coordination guidance in remediation task descriptions. Since the deployment context is `customer-shipped`, remediation tasks will include guidance about coordinating with Product Security for CVE assignment, advisory preparation, and formal disclosure.

## Version Impact Table

Based on simulated lock file data for quinn-proto:

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | |
| 2.1.1 | 0.11.9 | YES | |
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | |
| 2.2.4 | 0.11.14 | NO | |

The 2.1.x stream (versions 2.1.0, 2.1.1) is also affected, but this issue is scoped to 2.2.x only. Cross-stream impact will be addressed in Case A.

Within the issue's 2.2.x scope, versions 2.2.0, 2.2.1, and 2.2.2 are affected; versions 2.2.3 and 2.2.4 are not affected (ship quinn-proto 0.11.14, which is the fix version).
