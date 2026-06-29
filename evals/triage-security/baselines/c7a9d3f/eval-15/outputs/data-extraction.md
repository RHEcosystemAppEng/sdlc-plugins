# Step 1 -- Data Extraction

## Step 0 -- Configuration Validation

The project CLAUDE.md contains all required sections:

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345
- **ProdSec contact email** _(optional)_: prodsec-team@example.com
- **ProdSec Jira account ID** _(optional)_: 557058:prodsec-mock-account-id

Version Streams:
| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

Source Repositories:
| Repository | URL | Local Path |
|------------|-----|------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend |

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Stream scope | 2.2.x |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Due date | 2026-07-15 |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Reporter | psirt-analyst (account ID: 557058:psirt-analyst-mock-id) |
| Existing comments | None |

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. Based on the Ecosystem Mappings in both streams' security-matrix.md files, this maps to the **Cargo** ecosystem:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` (2.1.x) / `release/0.4.z` (2.2.x) |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream (Konflux release repo: `rhtpa-release.0.4.z`). This issue is stream-scoped to 2.2.x only. The 2.1.x stream is analyzed for cross-stream impact but Affects Versions corrections are scoped to 2.2.x.
