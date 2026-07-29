# Step 1 -- Data Extraction: TC-8021

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-55123 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches `pscomponent:` pattern from Security Configuration) |
| Product version (PSIRT-claimed) | rhtpa-2.1 | Summary suffix `[rhtpa-2.1]` |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.1.1 | Jira `versions` field |
| Vulnerable library | tokio | Description text |
| Affected version range | versions before 1.42.0 | Description text |
| Fixed version | 1.42.0 | Description text |
| CVSS | 8.1 (High) | Description text |
| Upstream fix PR | tokio-rs/tokio#7001 | Remote links (https://github.com/tokio-rs/tokio/pull/7001) |
| Advisory URL | GHSA-2026-tk91-v5pp | Remote links (https://github.com/advisories/GHSA-2026-tk91-v5pp) |
| CVE record URL | CVE-2026-55123 | Remote links (https://www.cve.org/CVERecord?id=CVE-2026-55123) |
| Due date | 2026-08-15 | Issue `duedate` field |
| Existing comments | None | Issue comment history |
| Upstream Affected Component | tokio | customfield_10632 |
| PS Component | pscomponent:org/rhtpa-server | customfield_10669 |
| Stream | rhtpa-2.1 | customfield_10832 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Mapped stream: **2.1.x**
- Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.3.z`
- Local path: `/home/dev/repos/rhtpa-release.0.3.z`
- Issue is **stream-scoped** to 2.1.x only

## Ecosystem Detection

- Library: tokio (Rust crate)
- Ecosystem: **Cargo** (source dependency)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.3.z`
- Classification: Source dependency -- 2 remediation tasks per stream (upstream backport + downstream propagation)

## Deployment Context

- Affected repository: rhtpa-backend (from component label `pscomponent:org/rhtpa-server`)
- Deployment context: `upstream` (default -- no Deployment Context column in Source Repositories table)

## Existing Preemptive Task Context

The issue description notes that a proactive remediation task TC-8022 already exists for this stream, created by a prior cross-stream triage of TC-8020 (stream rhtpa-2.2). This will be evaluated in Step 4.4.
