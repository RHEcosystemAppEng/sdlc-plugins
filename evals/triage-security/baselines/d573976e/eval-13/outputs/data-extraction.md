# Step 0 -- Validate Project Configuration

Configuration extracted from CLAUDE.md:

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345
- **Version Streams**: 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z)
- **Source Repositories**: rhtpa-backend (https://github.com/rhtpa/rhtpa-backend)
- **Deployment Context**: Not configured (column absent) -- defaulting all repos to `upstream`

## Step 0.3 -- Matrix Staleness Check

The security-matrix.md has `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-07-01, which is 3 days ago. This is within the 14-day default threshold. Proceeding without staleness warning.

## Step 1 -- Data Extraction

Parsed CVE data from Vulnerability issue TC-8001:

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
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

### Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the configured Version Stream **2.2.x**. Triage is scoped to the 2.2.x stream only.

### Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, the ecosystem is **Cargo**. The Cargo ecosystem uses `Cargo.lock` as the lock file and the check command is `git show <tag>:Cargo.lock`.

### Deployment Context Lookup

The affected component label `pscomponent:org/rhtpa-server` maps to repository `rhtpa-backend`. The Source Repositories table does not have a Deployment Context column, so the deployment context defaults to `upstream`.
