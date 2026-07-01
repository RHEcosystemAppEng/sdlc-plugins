# Step 0 -- Validate Project Configuration

Configuration extracted from CLAUDE.md:

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345
- **ProdSec contact email**: not configured (skip silently)
- **ProdSec Jira account ID**: not configured (skip @mentions silently)
- **Embargo policy URL**: not configured (skip Step 1.7 silently)
- **Upstream Affected Component custom field**: not configured (skip Steps 4.3 and 7)
- **PS Component custom field**: not configured
- **Stream custom field**: not configured

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories

| Repository | URL | Local Path |
|------------|-----|------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend |

The Source Repositories table does NOT have a Deployment Context column. Per backward compatibility rules, all repositories default to `upstream`. The Coordination Guidance subsection is omitted entirely from remediation task descriptions.

## Step 0.3 -- Matrix Staleness Check

The security-matrix.md has `Last-Updated: 2026-06-28T10:00:00Z`. Current date is 2026-07-01. The matrix is 3 days old, which is within the 14-day default threshold. Proceeding without staleness warning.

## Step 0.5 -- JIRA Access Initialization

(Simulated -- no actual Jira connection in eval mode.)

---

# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-33501 |
| Affected component | pscomponent:org/rhtpa-server (from labels) |
| Product version (PSIRT-claimed) | _(none -- no stream suffix in summary)_ |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | < 0.4.8 |
| Fixed version | 0.4.8 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/812 |
| Advisory URL | https://github.com/advisories/GHSA-2026-kv8p-r3n7 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-33501 |
| Due date | 2026-08-01 |
| Existing comments | _(none)_ |

## Stream Scope Resolution

The issue summary is "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames" -- there is **no** stream suffix in brackets. Therefore, this issue is treated as **unscoped**. Per the skill protocol, unscoped issues cover all streams. Steps 2-8 will analyze ALL versions across ALL configured streams (2.1.x and 2.2.x).

## Ecosystem Detection

The vulnerable library is `h2`, which is a Rust crate. Checking the Ecosystem Mappings tables from both streams' security-matrix.md files confirms that **Cargo** is a supported ecosystem with:
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Repository: backend
- Upstream Branch: `release/0.3.z` (stream 2.1.x) and `release/0.4.z` (stream 2.2.x)

Ecosystem: **Cargo** (source dependency).

## Deployment Context Lookup

The affected component label is `pscomponent:org/rhtpa-server`. Looking up the repository in the Source Repositories table: `rhtpa-backend` maps to URL `https://github.com/rhtpa/rhtpa-backend`.

The Source Repositories table does not include a Deployment Context column. Per backward compatibility rules, the deployment context defaults to `upstream`. Coordination Guidance will be omitted from remediation task descriptions.

## Step 1.5 -- External CVE Data Enrichment

(Simulated -- no actual WebFetch calls in eval mode.)

The Jira description provides a clear fix threshold: h2 < 0.4.8, fixed in 0.4.8. In a real triage, MITRE CVE API and OSV.dev would be queried to cross-validate. For this eval, using the Jira description data as the authoritative fix threshold: **h2 < 0.4.8, fixed in 0.4.8**.

## Step 1.7 -- Embargo Check

No Embargo policy URL is configured in Security Configuration. Step 1.7 is skipped silently.
