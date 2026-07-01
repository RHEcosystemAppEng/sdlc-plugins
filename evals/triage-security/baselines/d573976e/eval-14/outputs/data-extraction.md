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
- **Embargo policy URL**: not configured

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories

| Repository | URL | Local Path |
|------------|-----|------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend |

Note: The Source Repositories table does NOT have a Deployment Context column. All repositories default to `upstream`. Coordination guidance will be omitted from remediation task descriptions (backward compatibility).

## Step 0.3 -- Matrix Staleness Check

The security-matrix.md has `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-07-01. The matrix was last updated 3 days ago, which is within the 14-day default threshold. Proceeding without staleness warning.

## Step 0.5 -- JIRA Access Initialization

(Simulated -- no external tools called per eval instructions.)

## Step 1 -- Data Extraction

### Extracted CVE Data

| Field | Value |
|-------|-------|
| **CVE ID** | CVE-2026-40215 |
| **Affected component** | pscomponent:org/rhtpa-server (from label) |
| **Product version (PSIRT-claimed)** | [rhtpa-2.2] (from summary suffix) |
| **Affects Versions (Jira field)** | RHTPA 2.0.0 |
| **Vulnerable library** | openssl-libs |
| **Affected version range** | versions before 3.0.7-28.el9_4 |
| **Fixed version** | 3.0.7-28.el9_4 |
| **CVSS** | 7.1 (High) |
| **Upstream fix PR** | (none in remote links) |
| **Advisory URL** | https://access.redhat.com/errata/RHSA-2026:4021 |
| **CVE record URL** | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| **Due date** | 2026-08-15 |
| **Existing comments** | (none) |
| **Status** | New |

### Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`. Mapping to configured Version Streams:

- `[rhtpa-2.2]` maps to stream **2.2.x** (Konflux release repo: rhtpa-release.0.4.z)

**Issue stream scope**: 2.2.x -- triage is scoped to this stream only.

### Ecosystem Detection

The vulnerable library is **openssl-libs**, which is an RPM system package (not a Cargo crate or npm package). Checking the 2.2.x stream's Ecosystem Mappings table:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

RPM is listed in the Ecosystem Mappings table. The ecosystem is **RPM**.

For RPM packages:
- **Lock file**: `rpms.lock.yaml`
- **Check command**: `git show <tag>:rpms.lock.yaml`
- **Upstream Branch**: (none -- RPM ecosystem has no upstream branch)

This means remediation will follow the **system package path** (single task in Konflux release repo), not the two-task source dependency path.

### Deployment Context Lookup

The affected component label is `pscomponent:org/rhtpa-server`. Looking up the corresponding repository in the Source Repositories table:

The Source Repositories table does not have a Deployment Context column. Per the skill protocol, all repositories default to `upstream`. Coordination guidance will be omitted from remediation task descriptions.

## Step 1.5 -- External CVE Data Enrichment

(Simulated -- no external tools called per eval instructions.)

In a real triage, MITRE CVE API and OSV.dev would be queried for CVE-2026-40215. The Jira description provides a clear fix threshold (3.0.7-28.el9_4), so assuming external sources agree, the enriched fix threshold is **3.0.7-28.el9_4**.

## Step 1.7 -- Embargo Check

No Embargo policy URL is configured in Security Configuration. Skipping Step 1.7 silently.
