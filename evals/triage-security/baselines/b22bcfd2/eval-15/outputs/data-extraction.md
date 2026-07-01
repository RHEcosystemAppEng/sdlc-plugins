# Step 0 -- Validate Project Configuration

Configuration extracted from CLAUDE.md (`claude-md-security-config-prodsec.md`):

| Config Field | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| ProdSec contact email | prodsec-team@example.com |
| ProdSec Jira account ID | 557058:prodsec-mock-account-id |
| Embargo policy URL | _(not configured)_ |

**Source Repositories** (from Source Repositories table):
- rhtpa-backend -> { url: "https://github.com/rhtpa/rhtpa-backend", deployment_context: "upstream" }

Note: The Source Repositories table does NOT have a Deployment Context column. All repositories default to `upstream` per backward-compatible extraction (Step 0).

**Version Streams**:
- 2.1.x: Konflux Release Repo = git.example.com/rhtpa/rhtpa-release.0.3.z, Local Path = /home/dev/repos/rhtpa-release.0.3.z
- 2.2.x: Konflux Release Repo = git.example.com/rhtpa/rhtpa-release.0.4.z, Local Path = /home/dev/repos/rhtpa-release.0.4.z

## Step 0.3 -- Matrix Staleness Check

Security matrix `Last-Updated` timestamp: `2026-06-28T10:00:00Z`
Current date: 2026-07-01
Days since last update: 3 days

The matrix is within the 14-day freshness threshold. Proceeding without staleness warning.

---

# Step 1 -- Data Extraction

**Issue**: TC-8001
**Reporter**: psirt-analyst (account ID: 557058:psirt-analyst-mock-id)

## Extracted CVE Data

| Field | Value |
|---|---|
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
| Existing comments | (none) |

## Stream Scope Resolution

Issue summary contains stream suffix: `[rhtpa-2.2]`
Mapped to configured Version Stream: **2.2.x** (Konflux release repo: rhtpa-release.0.4.z)
Issue stream scope: **2.2.x only**

## Ecosystem Detection

Library: quinn-proto (Rust crate)
Ecosystem Mappings tables for both streams list **Cargo** as a supported ecosystem.
Detected ecosystem: **Cargo** (source dependency)

This means remediation will follow the two-task pattern: upstream backport task + downstream propagation subtask.

## Deployment Context Lookup

Affected repository from component label (pscomponent:org/rhtpa-server): rhtpa-backend
Deployment context: **upstream** (defaulted -- Source Repositories table has no Deployment Context column)
