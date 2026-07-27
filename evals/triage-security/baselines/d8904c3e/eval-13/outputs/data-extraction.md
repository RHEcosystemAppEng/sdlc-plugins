# Step 1 -- Data Extraction for TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration Version Streams table.

- Stream suffix: `[rhtpa-2.2]` -> stream **2.2.x**
- Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.4.z
- Local Path: /home/dev/repos/rhtpa-release.0.4.z

The issue is **stream-scoped** to 2.2.x. Steps 3-4 apply to this single stream, but all streams are analyzed for cross-stream impact (Case A).

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Category: Source dependency
- Remediation tasks per stream: 2 (upstream backport + downstream propagation)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`

## Deployment Context

- Source repository: rhtpa-backend
- URL: https://github.com/rhtpa/rhtpa-backend
- Deployment context: upstream (default -- no Deployment Context column in Source Repositories table)

## Affects Versions Discrepancy (Preliminary)

The current Affects Versions field lists **RHTPA 2.0.0**, which does not correspond to any version in either configured stream (2.1.x or 2.2.x). This will be corrected in Step 3 after the version impact analysis in Step 2.
