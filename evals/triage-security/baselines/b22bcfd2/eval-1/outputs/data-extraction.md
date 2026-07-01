# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Label matching component label pattern `pscomponent:` |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field (PSIRT-assigned) |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | < 0.11.14 | Description: "versions before 0.11.14" |
| Fixed version | 0.11.14 | Description: "Fixed version: 0.11.14" |
| CVSS | 7.5 (High) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links (GitHub Advisory) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comment history |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. Mapping to configured Version Streams:

- `[rhtpa-2.2]` maps to stream **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`)
- Issue stream scope: **2.2.x only**

Steps 2--8 will be scoped to the 2.2.x stream. The 2.1.x stream versions will be analyzed for completeness in the version impact table (Important Rule 4: check ALL supported versions), but Affects Versions correction and remediation tasks will be scoped to 2.2.x.

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. Checking the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

quinn-proto is a Rust crate, which maps to the **Cargo** ecosystem. Cargo is listed in the Ecosystem Mappings table, so automated triage can proceed.

- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`

## Deployment Context Lookup

The Source Repositories table in Security Configuration does not include a Deployment Context column. Per backward compatibility rules, all repositories default to `upstream`. No Coordination Guidance subsection will be included in remediation task descriptions.
