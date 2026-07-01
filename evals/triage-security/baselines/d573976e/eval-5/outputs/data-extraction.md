# Step 0 -- Validate Project Configuration

Configuration extracted from CLAUDE.md:

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345
- **Upstream Affected Component custom field**: not configured -- Step 4.3 will be skipped
- **PS Component custom field**: not configured
- **Stream custom field**: not configured
- **ProdSec contact email**: not configured
- **ProdSec Jira account ID**: not configured -- @mentions will be omitted
- **Embargo policy URL**: not configured -- Step 1.7 will be skipped
- **Source Repositories**: rhtpa-backend (https://github.com/rhtpa/rhtpa-backend). No Deployment Context column present -- defaulting all repositories to `upstream`. Coordination guidance subsection will be omitted from remediation tasks (backward compatibility).

**Version Streams:**

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

## Step 0.3 -- Matrix Staleness Check

Security matrix `Last-Updated` timestamp: `2026-06-28T10:00:00Z` (3 days ago as of 2026-07-01).

The matrix is within the 14-day default threshold. Proceeding without staleness warning.

## Step 1 -- Data Extraction

**Issue**: TC-8005
**Status**: New -- proceeding with full triage (default path).

Parsed CVE data from TC-8005:

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| Upstream fix PR | -- (none in remote links) |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Existing comments | none |
| CVSS | 7.1 (High) |

### Stream Scope Resolution

Issue summary suffix: `[rhtpa-2.2]` maps to stream **2.2.x** from the Version Streams table.

**Issue stream scope**: 2.2.x (scoped). Steps 3 and 8 will be scoped to the 2.2.x stream only.

### Ecosystem Detection

The vulnerable library is **openssl-libs**, a system-level RPM package (not a Cargo crate or npm module). The Ecosystem Mappings table for the 2.2.x stream lists:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

The **RPM** ecosystem matches openssl-libs. This is a system package ecosystem -- the lock file is `rpms.lock.yaml` and the check command is `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`.

**Detected ecosystem: RPM**

RPM is a system package ecosystem, so remediation will produce a **single task** (Konflux release repo fix), not the two-task upstream+downstream flow used for source dependency ecosystems (Cargo, npm).

### Deployment Context Lookup

The affected component label `pscomponent:org/rhtpa-server` maps to the rhtpa-backend repository. The Source Repositories table does not have a Deployment Context column. Defaulting to `upstream`. Coordination guidance will be omitted from remediation task descriptions.

## Step 1.5 -- External CVE Data Enrichment

> Note: External tools are not called in this eval. In a real triage, the MITRE CVE API and OSV.dev would be queried for CVE-2026-40215.

Based on the Jira description data:
- **Affected range**: versions before 3.0.7-28.el9_4
- **Fixed version**: 3.0.7-28.el9_4

Using Jira description data as the fix threshold for Step 2.3 comparisons.

## Step 1.7 -- Embargo Check

No Embargo policy URL is configured in Security Configuration. Skipping Step 1.7 silently.
