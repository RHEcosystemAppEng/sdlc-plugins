# Step 1 -- Data Extraction: TC-8003

## Extracted CVE Metadata

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x (mapped from suffix `[rhtpa-2.2]` to Version Streams table entry `2.2.x` at `git.example.com/rhtpa/rhtpa-release.0.4.z`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Upstream fix PR | Not provided in remote links |
| Due date | 2026-07-15 |
| Existing comments | None |
| Assignee | Unassigned |
| Status | New |

## Ecosystem Detection

- **Ecosystem**: Cargo (Rust crate -- quinn-proto is a Rust crate)
- **Category**: Source dependency
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`
- **Upstream branch**: `release/0.4.z` (for stream 2.2.x)
- **Remediation tasks per stream**: 2 (upstream backport + downstream propagation)

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the configured Version Stream `2.2.x` at Konflux release repo `git.example.com/rhtpa/rhtpa-release.0.4.z` (local path: `/home/dev/repos/rhtpa-release.0.4.z`).

This is a **scoped** issue -- Steps 3 and 4 apply only to the 2.2.x stream.

## Deployment Context

The affected repository `rhtpa-backend` is found in the Source Repositories table with URL `https://github.com/rhtpa/rhtpa-backend` and local path `/home/dev/repos/rhtpa-backend`. No Deployment Context column is present, so the default context is `upstream`.

## Version Impact Analysis (Step 2)

Using the security-matrix.md data for the 2.2.x stream (rhtpa-release.0.4.z), the quinn-proto versions at each pinned commit are:

| Version | Build Tag | quinn-proto Version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| RHTPA 2.2.0 | v0.4.5 | 0.11.9 | YES | 0.11.9 < 0.11.14 (fix threshold) |
| RHTPA 2.2.1 | v0.4.8 | 0.11.12 | YES | 0.11.12 < 0.11.14 (fix threshold) |
| RHTPA 2.2.2 | v0.4.9 | 0.11.12 | YES | Retag of v0.4.8 -- same as RHTPA 2.2.1 |
| RHTPA 2.2.3 | v0.4.11 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |
| RHTPA 2.2.4 | v0.4.12 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |

**Summary**: RHTPA 2.2.0, 2.2.1, and 2.2.2 are affected. RHTPA 2.2.3 and 2.2.4 ship the fixed version and are NOT affected. The fix was introduced at build tag v0.4.11 (quinn-proto 0.11.14).

## Also Checked: 2.1.x Stream (Cross-Stream Reference)

Although TC-8003 is scoped to the 2.2.x stream, for completeness in understanding the full CVE landscape:

| Version | Build Tag | quinn-proto Version | Affected? |
|---------|-----------|---------------------|-----------|
| RHTPA 2.1.0 | v0.3.8 | 0.11.9 | YES |
| RHTPA 2.1.1 | v0.3.12 | 0.11.9 | YES |

Both 2.1.x versions are affected, but they are outside the scope of TC-8003 (stream suffix [rhtpa-2.2]).
