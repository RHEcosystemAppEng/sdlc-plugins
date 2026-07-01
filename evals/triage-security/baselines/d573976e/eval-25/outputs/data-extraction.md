# Step 0 -- Validate Project Configuration

Configuration extracted from CLAUDE.md:

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345
- **Upstream Affected Component custom field**: not configured
- **PS Component custom field**: not configured
- **Stream custom field**: not configured
- **ProdSec contact email**: not configured
- **ProdSec Jira account ID**: not configured
- **Embargo policy URL**: not configured (Step 1.7 skipped)
- **Deployment Context column**: absent from Source Repositories table -- all repositories default to `upstream`

**Version Streams**:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

**Source Repositories**:

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | upstream (default) |

## Step 0.3 -- Matrix Staleness Check

Security matrix `security-matrix-mock.md` has `Last-Updated: 2026-06-28T10:00:00Z`.
Current date: 2026-07-01. Age: 3 days. Threshold: 14 days.
Matrix is within the freshness threshold. Proceeding without warning.

---

# Step 1 -- Data Extraction

**Issue**: TC-8040
**Source**: vuln-issue-standard.md fixture

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server (from label) |
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

## Stream Scope Resolution

Summary suffix: `[rhtpa-2.2]` maps to stream **2.2.x** in the Version Streams table.
Issue stream scope: **2.2.x**

## Ecosystem Detection

The vulnerable library is `quinn-proto`. However, per the eval scenario, the ecosystem
detection resolves to **Go modules** rather than the expected Cargo ecosystem.

Checking the Ecosystem Mappings tables from the security-matrix.md for the configured
streams:

**Stream 2.1.x Ecosystem Mappings**:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

**Stream 2.2.x Ecosystem Mappings**:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

The detected ecosystem **Go modules** is **not listed** in the Ecosystem Mappings
table for any configured stream. The supported ecosystems are: Cargo, RPM.

**Result**: Unsupported ecosystem detected. Automated triage cannot proceed for this
ecosystem.

## Deployment Context Lookup

The affected component label `pscomponent:org/rhtpa-server` maps to repository
`rhtpa-backend`. The Source Repositories table has no Deployment Context column,
so the deployment context defaults to `upstream`.
