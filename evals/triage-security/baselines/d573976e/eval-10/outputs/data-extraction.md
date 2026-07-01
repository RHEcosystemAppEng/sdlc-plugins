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
| Upstream Affected Component field | customfield_10632 |
| PS Component field | customfield_10669 |
| Stream field | customfield_10832 |
| ProdSec contact email | _(not configured)_ |
| ProdSec Jira account ID | _(not configured)_ |
| Embargo policy URL | _(not configured)_ |

Version Streams:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

Source Repositories:

| Repository | URL | Local Path | Deployment Context |
|------------|-----|------------|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | upstream _(default -- no Deployment Context column in config)_ |

## Step 0.3 -- Matrix Staleness Check

Security matrix `security-matrix-mock.md` has `Last-Updated: 2026-06-28T10:00:00Z` (3 days ago as of 2026-07-01). This is within the 14-day threshold. Proceeding without staleness warning.

## Step 0.5 -- JIRA Access Initialization

_(Skipped per eval instructions -- no external tool calls)_

---

# Step 1 -- Data Extraction

Issue: **TC-8020**

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Affected component | pscomponent:org/rhtpa-server (from label) |
| Product version (PSIRT-claimed) | [rhtpa-2.2] (from summary suffix) |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable library | tokio |
| Affected version range | < 1.42.0 |
| Fixed version | 1.42.0 |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 |
| Advisory URL | https://github.com/advisories/GHSA-2026-tk91-v5pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Due date | 2026-08-15 |
| CVSS | 8.1 (High) |
| Existing comments | _(none)_ |
| Upstream Affected Component | tokio (customfield_10632) |
| PS Component | pscomponent:org/rhtpa-server (customfield_10669) |
| Stream | rhtpa-2.2 (customfield_10832) |

### Stream Scope Resolution

Summary suffix: `[rhtpa-2.2]` maps to stream **2.2.x** from the Version Streams table. This issue is **scoped** to the 2.2.x stream. Steps 3 and 8 will be scoped to 2.2.x versions only. Cross-stream analysis (Case B) will check other streams for impact.

### Ecosystem Detection

The vulnerable library is **tokio**, a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's `security-matrix.md`, the ecosystem is **Cargo**. Lock file: `Cargo.lock`. Check command: `git show <tag>:Cargo.lock`.

### Deployment Context Lookup

Repository `rhtpa-backend` does not have a Deployment Context column in the Source Repositories table. Defaulting to **upstream**.

## Step 1.5 -- External CVE Data Enrichment

_(In a real triage, WebFetch would query MITRE CVE API and OSV.dev. Per eval instructions, no external tools are called. The fixture provides structured data: affected versions < 1.42.0, fixed version 1.42.0.)_

Using Jira description data as the authoritative fix threshold: **1.42.0**.

## Step 1.7 -- Embargo Check

No Embargo policy URL is configured in Security Configuration. Step 1.7 is skipped silently.
