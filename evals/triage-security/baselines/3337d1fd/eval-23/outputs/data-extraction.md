# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| CVSS | 7.5 (High) |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream
(Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

This issue is **stream-scoped** to 2.2.x. Steps 3 and 4 will apply only to versions within
the 2.2.x stream. Cross-stream impact on 2.1.x is handled in Case B (Step 8).

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. The ecosystem is **Cargo**.

From the 2.2.x stream's Ecosystem Mappings:
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`
- Repository: backend

## Deployment Context Lookup

The component label `pscomponent:org/rhtpa-server` maps to repository **rhtpa-backend** in the
Source Repositories table.

| Repository | URL | Local Path | Deployment Context |
|------------|-----|------------|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | **customer-shipped** |

Deployment context: **customer-shipped**

This deployment context will be used in Step 8 (Remediation) to generate coordination guidance
in remediation task descriptions. Per the remediation templates, customer-shipped components
require coordination with Product Security for CVE assignment, advisory preparation, and formal
disclosure.

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

### Summary

- **2.2.x stream** (issue scope): versions 2.2.0, 2.2.1, 2.2.2 are affected; 2.2.3 and 2.2.4 are not affected
- **2.1.x stream** (cross-stream): versions 2.1.0 and 2.1.1 are affected (will be reported in Case B)
- The PSIRT-assigned Affects Versions (`RHTPA 2.0.0`) is incorrect -- there is no 2.0 stream. The correct Affects Versions for the 2.2.x stream scope are: `RHTPA 2.2.0`, `RHTPA 2.2.1`, `RHTPA 2.2.2`
