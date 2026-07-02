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
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Assignee | Unassigned |
| Status | New |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.1]`.

- Parsed suffix: `rhtpa-2.1` maps to stream `2.1.x`
- Matched Version Stream: `2.1.x` at `git.example.com/rhtpa/rhtpa-release.0.3.z` (local path: `/home/dev/repos/rhtpa-release.0.3.z`)
- Issue stream scope: **2.1.x only** (scoped issue -- Steps 2-8 apply only to this stream)

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Source repository: backend
- Upstream branch: `release/0.3.z`

## Deployment Context

- Affected repository from component label: rhtpa-server (mapped from `pscomponent:org/rhtpa-server`)
- Source Repositories lookup: rhtpa-backend found at `https://github.com/rhtpa/rhtpa-backend`
- Deployment context: `upstream` (default -- no explicit Deployment Context column in configuration)

## Existing Issue Links

| Link Type | Direction | Linked Issue | Summary |
|-----------|-----------|--------------|---------|
| Related | outward (this issue -> TC-8001) | TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |

Link ID: 1990401

## Remote Links

| Title | URL |
|-------|-----|
| GHSA-2026-qp73-x4mq | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE-2026-31812 | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
