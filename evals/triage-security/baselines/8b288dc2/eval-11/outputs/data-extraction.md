# Step 1 -- Data Extraction: TC-8021

## Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-55123 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Label matching `pscomponent:` pattern |
| Product version (PSIRT-claimed) | rhtpa-2.1 | Summary suffix `[rhtpa-2.1]` |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.1.1 | Jira `versions` field |
| Vulnerable library | tokio | Description text |
| Affected version range | versions before 1.42.0 | Description text |
| Fixed version | 1.42.0 | Description text |
| CVSS | 8.1 (High) | Description text |
| Upstream fix PR | tokio-rs/tokio#7001 | Remote links |
| Advisory URL | GHSA-2026-tk91-v5pp | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 | Remote links |
| Due date | 2026-08-15 | Issue `duedate` field |
| Existing comments | None | Issue comment history |

## Custom Fields

| Field | Value |
|-------|-------|
| Upstream Affected Component (customfield_10632) | tokio |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-server |
| Stream (customfield_10832) | rhtpa-2.1 |

## Stream Scope Resolution

- Issue summary suffix: `[rhtpa-2.1]`
- Mapped to Version Stream: **2.1.x** (Konflux release repo: `rhtpa-release.0.3.z`)
- This issue is **stream-scoped** -- Steps 3-8 apply only to the 2.1.x stream

## Ecosystem Detection

- Library: tokio (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.3.z` (from 2.1.x stream Ecosystem Mappings)

## Deployment Context Lookup

- Affected repository: rhtpa-backend (resolved from component label `pscomponent:org/rhtpa-server`)
- Source Repositories table entry: rhtpa-backend at https://github.com/rhtpa/rhtpa-backend
- Deployment Context column: not present in configuration (absent)
- Deployment context: **upstream** (default, since Deployment Context column is absent)
