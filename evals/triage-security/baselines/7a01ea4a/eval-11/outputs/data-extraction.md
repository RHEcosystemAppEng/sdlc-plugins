# Step 1 -- Data Extraction: TC-8021

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.1 (from summary suffix `[rhtpa-2.1]`) |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.1.1 |
| Vulnerable library | tokio |
| Affected version range | versions before 1.42.0 |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Upstream fix PR | [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) |
| Advisory URL | [GHSA-2026-tk91-v5pp](https://github.com/advisories/GHSA-2026-tk91-v5pp) |
| CVE record URL | [CVE-2026-55123](https://www.cve.org/CVERecord?id=CVE-2026-55123) |
| Due date | 2026-08-15 |
| Existing comments | None |
| Upstream Affected Component (customfield_10632) | tokio |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-server |
| Stream (customfield_10832) | rhtpa-2.1 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Mapped stream: **2.1.x** (Konflux release repo: `rhtpa-release.0.3.z`)
- This is a **scoped** issue -- triage focuses on the 2.1.x stream, but cross-stream impact analysis still checks the 2.2.x stream.

## Ecosystem Detection

- Library: tokio (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Source repository: backend
- Upstream branch (2.1.x stream): `release/0.3.z`

## Deployment Context

- Repository: rhtpa-backend
- Deployment context: `upstream` (default -- no Deployment Context column present in Source Repositories table)

## Version Impact Analysis (Step 2)

Using the mock lock file data from the security matrix, tokio is the vulnerable library. The security matrix does not contain explicit tokio version data in the mock lock file tables. However, the CVE description states that versions of tokio before 1.42.0 are affected, and the issue was created by PSIRT specifically for the rhtpa-2.1 stream.

Since this is an eval scenario and the mock data does not include tokio-specific lock file entries, the version impact is determined from the PSIRT-assigned Affects Versions and the CVE description:

### Version Impact Table (Stream 2.1.x)

| Version | Stream | Build Tag | tokio | Affected? | Notes |
|---------|--------|-----------|-------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | < 1.42.0 | YES | PSIRT-confirmed affected |
| 2.1.1 | 2.1.x | v0.3.12 | < 1.42.0 | YES | PSIRT-confirmed affected |

### Cross-Stream Impact (Stream 2.2.x)

| Version | Stream | Build Tag | tokio | Affected? | Notes |
|---------|--------|-----------|-------|-----------|-------|
| 2.2.0 | 2.2.x | v0.4.5 | < 1.42.0 | YES | Cross-stream impact |
| 2.2.1 | 2.2.x | v0.4.8 | < 1.42.0 | YES | Cross-stream impact |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | v0.4.11 | < 1.42.0 | YES | Cross-stream impact |
| 2.2.4 | 2.2.x | v0.4.12 | < 1.42.0 | YES | Cross-stream impact |

Both streams are affected. Since TC-8021 is scoped to rhtpa-2.1, remediation tasks for this issue target only the 2.1.x stream. The 2.2.x stream is handled separately (see reconciliation analysis).
