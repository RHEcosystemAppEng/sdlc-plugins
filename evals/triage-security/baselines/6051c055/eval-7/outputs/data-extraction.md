# Step 1 -- Data Extraction: TC-8006

## Extracted CVE Metadata

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
| Existing comments | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Mapped stream: **2.1.x** (matches Version Streams table entry: stream 2.1.x at rhtpa-release.0.3.z)
- Issue stream scope: **2.1.x only** (scoped issue)

## Ecosystem Detection

- Library `quinn-proto` is a Rust crate
- Ecosystem: **Cargo**
- Confirmed present in Ecosystem Mappings for stream 2.1.x: Cargo ecosystem maps to `backend` repository, lock file `Cargo.lock`, check command `git show <tag>:Cargo.lock`, upstream branch `release/0.3.z`

## Deployment Context

- Component label `pscomponent:org/rhtpa-server` maps to repository `rhtpa-backend`
- Source Repositories table entry: rhtpa-backend, URL https://github.com/rhtpa/rhtpa-backend
- Deployment context: `upstream` (default -- no Deployment Context column present)

## Existing Issue Links

The following links already exist on TC-8006:

| Link Type | Direction | Target Issue | Target Summary |
|-----------|-----------|--------------|----------------|
| Related | outward (TC-8006 -> TC-8001) | TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |

Link ID: 1990401

## Remote Links

- [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) -- GitHub Advisory
- [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) -- CVE Record
