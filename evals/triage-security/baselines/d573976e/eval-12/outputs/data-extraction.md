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
- **Version Streams**:
  - 2.1.x: Konflux Release Repo `git.example.com/rhtpa/rhtpa-release.0.3.z`, Local Path `/home/dev/repos/rhtpa-release.0.3.z`
  - 2.2.x: Konflux Release Repo `git.example.com/rhtpa/rhtpa-release.0.4.z`, Local Path `/home/dev/repos/rhtpa-release.0.4.z`
- **Source Repositories**:
  - rhtpa-backend: URL `https://github.com/rhtpa/rhtpa-backend`, Local Path `/home/dev/repos/rhtpa-backend`
  - Deployment Context: not configured (column absent), default to `upstream`

## Step 0.3 -- Matrix Staleness Check

Security matrix `Last-Updated` timestamp: `2026-06-28T10:00:00Z`
Current date: 2026-07-01
Days since last update: 3 days
Threshold: 14 days

Result: Matrix is fresh (3 days < 14 days). Proceeding without staleness warning.

## Step 1 -- Data Extraction

**Issue**: TC-8030
**Summary**: CVE-2026-48901 h2 - HTTP/2 CONTINUATION flood [rhtpa-2.2]

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-48901 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0 | Jira `versions` field |
| Vulnerable library | h2 | Description text ("A vulnerability was found in h2") |
| Affected version range | "versions prior to the fix" (imprecise -- no specific version threshold) | Description text |
| Fixed version | "see advisory" (imprecise -- no specific version stated) | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 | Remote links |
| Due date | 2026-08-01 | Issue `duedate` field |
| Existing comments | None | Issue comment history |

**Note**: The Jira description does NOT provide a precise affected version range or fixed version. The description states "versions prior to the fix" and "see advisory" -- these are imprecise and insufficient for version impact analysis. Step 1.5 (External CVE Data Enrichment) is critical for this issue to obtain machine-readable fix thresholds.

### Stream scope resolution

Summary suffix: `[rhtpa-2.2]` maps to stream **2.2.x** in the Version Streams table.
Issue stream scope: **2.2.x** (scoped issue -- Steps 3 and 8 apply only to this stream).

### Ecosystem detection

Library: h2 (Rust crate, listed in the Cargo ecosystem in the Ecosystem Mappings table)
Ecosystem: **Cargo**

The Ecosystem Mappings table for both streams lists Cargo with:
- Repository: backend
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z` (for 2.2.x stream)

### Deployment context lookup

Repository `rhtpa-backend` found in Source Repositories table. Deployment Context column is absent (backward compatibility) -- default to `upstream`. Coordination guidance subsection will be omitted from remediation task descriptions.
