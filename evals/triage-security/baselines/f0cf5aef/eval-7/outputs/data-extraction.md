# Step 1 -- Data Extraction: TC-8006

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.1] |
| Affects Versions (Jira field) | RHTPA 2.1.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Assignee | Unassigned |
| Status | New |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.1]`. Mapping to configured Version Streams:

- `[rhtpa-2.1]` maps to stream **2.1.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.3.z`, local path: `/home/dev/repos/rhtpa-release.0.3.z`)

The issue is **stream-scoped** to the 2.1.x stream. Steps 3-4 will be scoped to this single stream.

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. Per the security-matrix.md Ecosystem Mappings table for the 2.1.x stream, the ecosystem is **Cargo**.

- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.3.z`
- Category: Source dependency
- Remediation tasks per stream: 2 (upstream backport + downstream propagation)

## Existing Issue Links

| Link Type | Direction | Linked Issue | Summary |
|-----------|-----------|--------------|---------|
| Related | outward (TC-8006 -> TC-8001) | TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |

Link ID: 1990401

## Remote Links

| Title | URL |
|-------|-----|
| GHSA-2026-qp73-x4mq | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE-2026-31812 | https://www.cve.org/CVERecord?id=CVE-2026-31812 |

## Deployment Context Lookup

The affected repository (rhtpa-backend) is found in the Source Repositories table. No Deployment Context column is present, so defaulting to `upstream`.
