# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.1] |
| Affects Versions (Jira field) | RHTPA 2.1.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | (none listed) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | (none) |
| Status | New |
| Assignee | Unassigned |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.1]`. Mapping to configured Version Streams:

- Suffix `[rhtpa-2.1]` maps to stream **2.1.x**
- Matched Version Stream: `2.1.x` at Konflux release repo `git.example.com/rhtpa/rhtpa-release.0.3.z` (local path `/home/dev/repos/rhtpa-release.0.3.z`)

The issue is **stream-scoped** to 2.1.x. Steps 3-4 will be scoped to this single stream.

## Ecosystem Detection

- Vulnerable library: quinn-proto (Rust crate)
- Detected ecosystem: **Cargo**
- Confirmed in the 2.1.x stream's Ecosystem Mappings table: Cargo ecosystem is configured with lock file `Cargo.lock` and check command `git show <tag>:Cargo.lock`
- Source repository: backend
- Upstream branch: `release/0.3.z`

## Deployment Context

- Repository `rhtpa-backend` found in Source Repositories table
- Deployment context: `upstream` (default -- no Deployment Context column present)

## Existing Issue Links

The following links already exist on TC-8006:

| Link Type | Direction | Linked Issue | Summary |
|-----------|-----------|--------------|---------|
| Related | outward (TC-8006 -> TC-8001) | TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |

Link ID: 1990401

## Remote Links

| Title | URL |
|-------|-----|
| GHSA-2026-qp73-x4mq | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE-2026-31812 | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
