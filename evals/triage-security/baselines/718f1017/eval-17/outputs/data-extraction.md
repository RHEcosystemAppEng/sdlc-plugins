# Step 1 -- Data Extraction for TC-8001

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches Component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links (quinn-rs/quinn#2048) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links (GHSA) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links (cve.org) |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comment history |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`.

- Parsed suffix: `rhtpa-2.2` maps to stream **2.2.x**
- Matched to Version Streams table: stream `2.2.x` at `git.example.com/rhtpa/rhtpa-release.0.4.z`
- **Issue stream scope**: 2.2.x (scoped to this single stream)

Steps 3-7 will be scoped to the 2.2.x stream only.

## Ecosystem Detection

- Vulnerable library: **quinn-proto** (a Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock` (per Ecosystem Mappings for stream 2.2.x)
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`

This is a source dependency ecosystem. Remediation will require **two tasks**: an upstream backport task (fix in the source repo) and a downstream propagation subtask (update the reference in the Konflux release repo).

## Affects Versions Discrepancy (Preliminary)

The PSIRT-assigned Affects Versions field says **RHTPA 2.0.0**, but there is no 2.0.x stream configured in the Version Streams table. The configured streams are 2.1.x and 2.2.x. This will need correction in Step 3 after version impact analysis confirms which versions are actually affected.
