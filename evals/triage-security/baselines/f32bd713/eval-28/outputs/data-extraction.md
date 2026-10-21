# Step 1 -- Data Extraction for TC-8060

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99010 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | < 0.4.5 (versions before 0.4.5) |
| Fixed version | 0.4.5 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 |
| Advisory URL | -- |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99010 |
| Due date | 2026-08-15 |
| Reporter | psirt-analyst (557058:psirt-analyst-mock-id) |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. This maps to the **2.2.x** stream from the Version Streams table in Security Configuration.

- Parsed suffix: `[rhtpa-2.2]` -> stream `2.2.x`
- Matched Version Stream: 2.2.x (Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.4.z)
- Issue stream scope: **2.2.x only**

Triage is scoped to the 2.2.x stream. Other streams (2.1.x) will be checked for cross-stream impact (Case A) but remediation tasks are created only for the scoped stream.

## Ecosystem Detection

The vulnerable library `h2` is a Rust crate. Based on the 2.2.x stream's Ecosystem Mappings table, this falls under the **Cargo** ecosystem.

- Ecosystem: **Cargo** (source dependency)
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`
- Repository: backend
- Classification: Source dependency -- produces **2 tasks** per affected stream (upstream fix + downstream propagation)

## Deployment Context

The Source Repositories table for `rhtpa-backend` does not include a Deployment Context column. Default: `upstream`. Coordination guidance subsection is omitted per backward compatibility rules.
