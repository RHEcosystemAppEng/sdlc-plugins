# Step 1 -- Data Extraction for TC-8021

## Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-55123 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Label matching component label pattern `pscomponent:` |
| Product version (PSIRT-claimed) | rhtpa-2.1 | Summary suffix `[rhtpa-2.1]` |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.1.1 | Jira `versions` field |
| Vulnerable library | tokio | Description text |
| Affected version range | versions before 1.42.0 (< 1.42.0) | Description text |
| Fixed version | 1.42.0 | Description text |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-tk91-v5pp | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 | Remote links |
| Due date | 2026-08-15 | Issue `duedate` field |
| Existing comments | None | Issue comment history |
| CVSS | 8.1 (High) | Description text |

## Custom Fields

| Field | Value |
|-------|-------|
| Upstream Affected Component (customfield_10632) | tokio |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-server |
| Stream (customfield_10832) | rhtpa-2.1 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Mapped stream: **2.1.x** (from Version Streams table: 2.1.x -> rhtpa-release.0.3.z)
- Issue stream scope: **scoped to stream 2.1.x only**
- Steps 3-7 will be scoped to the 2.1.x stream

## Ecosystem Detection

- Vulnerable library: tokio (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock` (per Ecosystem Mappings for the 2.1.x stream)
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.3.z`
- Repository: backend

## Issue Links

No existing issue links on TC-8021.

## Remote Links

1. [GHSA-2026-tk91-v5pp](https://github.com/advisories/GHSA-2026-tk91-v5pp) -- GitHub Advisory
2. [CVE-2026-55123](https://www.cve.org/CVERecord?id=CVE-2026-55123) -- CVE Record
3. [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) -- Upstream fix PR

## Vulnerability Summary

A use-after-free vulnerability in the tokio crate. Versions of tokio before 1.42.0 are vulnerable to a use-after-free when a spawned task is aborted while holding a borrowed reference. This can lead to memory corruption and potential code execution.
