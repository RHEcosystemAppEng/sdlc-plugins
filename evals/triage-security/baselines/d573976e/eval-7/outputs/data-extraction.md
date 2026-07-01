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
- **Embargo policy URL**: not configured (Step 1.7 will be skipped)
- **Version Streams**:
  - 2.1.x: Konflux Release Repo git.example.com/rhtpa/rhtpa-release.0.3.z, Local Path /home/dev/repos/rhtpa-release.0.3.z
  - 2.2.x: Konflux Release Repo git.example.com/rhtpa/rhtpa-release.0.4.z, Local Path /home/dev/repos/rhtpa-release.0.4.z
- **Source Repositories**:
  - rhtpa-backend: URL https://github.com/rhtpa/rhtpa-backend, Local Path /home/dev/repos/rhtpa-backend
  - Deployment Context column: absent (backward compatibility) -- default all repos to `upstream`

## Step 0.3 -- Matrix Staleness Check

Security matrix `Last-Updated` timestamp: `2026-06-28T10:00:00Z`
Current date: 2026-07-01
Days since last update: 3 days
Threshold: 14 days

Result: Matrix is fresh (3 days < 14 days). Proceeding without warning.

## Step 1 -- Data Extraction

Issue: **TC-8006**

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.1] |
| Affects Versions (Jira field) | RHTPA 2.1.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| Upstream fix PR | (not provided in remote links) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | (none) |
| CVSS | 7.5 (High) |
| Status | New |
| Assignee | Unassigned |

### Stream scope resolution

The issue summary contains stream suffix `[rhtpa-2.1]`.
- Parsed suffix: `rhtpa-2.1` maps to stream **2.1.x**
- Match: stream 2.1.x is configured in Version Streams table
- **Issue stream scope**: 2.1.x only

### Ecosystem detection

The vulnerable library is **quinn-proto**, a Rust crate. The 2.1.x stream's Ecosystem Mappings table includes Cargo with repository `backend` and lock file `Cargo.lock`.

**Detected ecosystem**: Cargo

### Deployment context lookup

Affected repository from component label `pscomponent:org/rhtpa-server` maps to `rhtpa-backend` in Source Repositories. The Source Repositories table does NOT have a Deployment Context column. Per backward compatibility rules, deployment context defaults to `upstream`. Coordination Guidance subsection will be omitted from remediation task descriptions.

### Existing issue links

The issue already has the following links:

- **Related**: TC-8001 (outward link, Link ID 1990401)
  - TC-8001 summary: CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]

### Step 1.7 -- Embargo Check

Embargo policy URL is not configured in Security Configuration. Step 1.7 is skipped silently.
