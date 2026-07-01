# Step 0 -- Validate Project Configuration

Configuration validated from CLAUDE.md:

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345
- **Upstream Affected Component custom field**: customfield_10632
- **PS Component custom field**: customfield_10669
- **Stream custom field**: customfield_10832
- **ProdSec contact email**: _(not configured)_
- **ProdSec Jira account ID**: _(not configured)_
- **Embargo policy URL**: _(not configured)_

**Version Streams:**

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

**Source Repositories:**

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | upstream _(default -- no Deployment Context column)_ |

## Step 0.3 -- Matrix Staleness Check

Security matrix `Last-Updated: 2026-06-28T10:00:00Z` -- this is 3 days ago (well within the 14-day threshold). No staleness warning. Proceeding.

## Step 0.5 -- JIRA Access Initialization

_(Skipped -- eval does not call external tools.)_

---

# Step 1 -- Data Extraction

**Issue**: TC-8021

Fetched via `jira.get_issue(TC-8021)` and `jira.get_issue_remote_links(TC-8021)`.

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Affected component | pscomponent:org/rhtpa-server (from label) |
| Product version (PSIRT-claimed) | [rhtpa-2.1] (from summary suffix) |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.1.1 |
| Vulnerable library | tokio |
| Affected version range | < 1.42.0 |
| Fixed version | 1.42.0 |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 |
| Advisory URL | https://github.com/advisories/GHSA-2026-tk91-v5pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Due date | 2026-08-15 |
| CVSS | 8.1 (High) |
| Existing comments | _(none)_ |
| Reporter | _(from Jira issue reporter field)_ |
| Upstream Affected Component (customfield_10632) | tokio |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-server |
| Stream (customfield_10832) | rhtpa-2.1 |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.1]`. Mapping to configured Version Streams:
- `[rhtpa-2.1]` maps to stream **2.1.x** (Konflux release repo: rhtpa-release.0.3.z)

**Issue stream scope**: 2.1.x only. Steps 3 and 4 will be scoped to this stream.

## Ecosystem Detection

The vulnerable library is **tokio**, a Rust crate. Based on the Ecosystem Mappings table in the 2.1.x stream's security-matrix.md, the **Cargo** ecosystem is configured with:
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.3.z`

**Detected ecosystem**: Cargo (source dependency)

## Deployment Context Lookup

Repository `rhtpa-backend` is in the Source Repositories table. The Source Repositories table does not have a Deployment Context column, so the default context is **upstream**.
