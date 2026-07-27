# Step 1 -- Data Extraction

## Source Issue

- **Issue Key**: TC-8021
- **Issue Type**: Vulnerability
- **Status**: New

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-55123 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches `pscomponent:` pattern from Security Configuration) |
| Product version (PSIRT-claimed) | rhtpa-2.1 | Summary suffix `[rhtpa-2.1]` |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.1.1 | Jira `versions` field |
| Vulnerable library | tokio | Description (`customfield_10632`: tokio) |
| Affected version range | versions before 1.42.0 | Description text |
| Fixed version | 1.42.0 | Description text |
| CVSS | 8.1 (High) | Description text |
| Upstream fix PR | tokio-rs/tokio#7001 | Remote links (https://github.com/tokio-rs/tokio/pull/7001) |
| Advisory URL | GHSA-2026-tk91-v5pp | Remote links (https://github.com/advisories/GHSA-2026-tk91-v5pp) |
| CVE record URL | CVE-2026-55123 | Remote links (https://www.cve.org/CVERecord?id=CVE-2026-55123) |
| Due date | 2026-08-15 | Issue `duedate` field |
| Existing comments | None | No comments on the issue |
| Existing issue links | None | No existing issue links |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Mapped stream: **2.1.x** (matches Version Streams row: `2.1.x` at `git.example.com/rhtpa/rhtpa-release.0.3.z`)
- Issue stream scope: **scoped to 2.1.x only**

## Ecosystem Detection

- Vulnerable library: **tokio** (Rust crate)
- Detected ecosystem: **Cargo** (source dependency)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.3.z`
- Classification: Source dependency -- remediation requires 2 tasks per stream (upstream backport + downstream propagation)

## Deployment Context Lookup

- Affected repository: rhtpa-backend (from pscomponent:org/rhtpa-server)
- Deployment context: `upstream` (default -- no Deployment Context column in Source Repositories table)

## Custom Fields

| Custom Field | Value |
|---|---|
| customfield_10632 (Upstream Affected Component) | tokio |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-server |
| customfield_10832 (Stream) | rhtpa-2.1 |
