# Step 0 -- Validate Project Configuration

## Configuration Extracted

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345
- **Embargo policy URL**: _(not configured -- Step 1.7 skipped)_
- **ProdSec contact email**: _(not configured)_
- **ProdSec Jira account ID**: _(not configured -- @mentions skipped)_
- **Upstream Affected Component custom field**: _(not configured -- Step 4.3 skipped)_
- **PS Component custom field**: _(not configured)_
- **Stream custom field**: _(not configured)_

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories (with Deployment Context)

| Repository | URL | Local Path | Deployment Context |
|------------|-----|------------|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | customer-shipped |

The Source Repositories table includes a **Deployment Context** column. The repository `rhtpa-backend` has deployment context **customer-shipped**. This value is recorded for use in Step 8 remediation task descriptions (Coordination Guidance subsection).

## Step 0.3 -- Matrix Staleness Check

The security-matrix.md contains `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`. Today is 2026-07-01. The matrix was last updated 3 days ago, which is within the 14-day default threshold. Proceeding without staleness warning.

---

# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |
| Issue status | New |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. Mapping to configured Version Streams:
- `rhtpa-2.2` maps to stream **2.2.x** (Konflux release repo: rhtpa-release.0.4.z)

**Issue stream scope**: 2.2.x (Steps 3 and 8 will be scoped to this stream only)

## Ecosystem Detection

The vulnerable library is **quinn-proto**, which is a Rust crate. The 2.2.x stream's Ecosystem Mappings table lists **Cargo** as a configured ecosystem with:
- Repository: backend
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`

**Detected ecosystem**: Cargo

## Deployment Context Lookup

The component label `pscomponent:org/rhtpa-server` maps to the source repository **rhtpa-backend**. Looking up the deployment context from the Source Repositories table:

- Repository: rhtpa-backend
- Deployment Context: **customer-shipped**

This deployment context is recorded as part of the CVE metadata and will be used in Step 8 (Remediation) to generate Coordination Guidance in remediation task descriptions.
