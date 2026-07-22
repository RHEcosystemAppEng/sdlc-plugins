# Data Extraction — TC-8020

## Step 1: Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable library | tokio |
| Affected version range | versions before 1.42.0 |
| Fixed version | 1.42.0 |
| Upstream fix PR | [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) |
| Advisory URL | [GHSA-2026-tk91-v5pp](https://github.com/advisories/GHSA-2026-tk91-v5pp) |
| CVE record URL | [CVE-2026-55123](https://www.cve.org/CVERecord?id=CVE-2026-55123) |
| CVSS | 8.1 (High) |
| Due date | 2026-08-15 |
| Existing comments | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry for stream `2.2.x` at `git.example.com/rhtpa/rhtpa-release.0.4.z`)
- Issue stream scope: **rhtpa-2.2** (scoped to single stream)

## Ecosystem Detection

- Ecosystem: **Cargo** (Rust crate — tokio is a Rust crate)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Source dependency: Yes (Cargo ecosystem requires 2-task remediation: upstream backport + downstream propagation)

## Deployment Context Lookup

- Affected repository: rhtpa-backend (from component label `pscomponent:org/rhtpa-server`)
- Deployment Context column: **absent** from Source Repositories table
- Default: `upstream`
- Coordination guidance: omitted (Deployment Context column absent — backward compatibility)

## Custom Fields

| Custom Field | Field ID | Value |
|---|---|---|
| Upstream Affected Component | customfield_10632 | tokio |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-server |
| Stream | customfield_10832 | rhtpa-2.2 |
