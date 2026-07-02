# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.1] |
| Affects Versions (Jira field) | RHTPA 2.1.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| Upstream fix PR | (none found in remote links) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| CVSS | 7.5 (High) |
| Due date | 2026-07-15 |
| Existing comments | (none) |
| Existing issue links | Related: TC-8001 (outward, link ID 1990401) |

## Stream Scope Resolution

- Issue summary suffix: `[rhtpa-2.1]`
- Mapped to configured Version Stream: **2.1.x** (Konflux release repo: git.example.com/rhtpa/rhtpa-release.0.3.z, local path: /home/dev/repos/rhtpa-release.0.3.z)
- Issue is **stream-scoped** to 2.1.x only

## Ecosystem Detection

- Vulnerable library: quinn-proto (a Rust crate)
- Detected ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Source repository: backend (upstream branch: `release/0.3.z` for stream 2.1.x)

## Deployment Context

- Affected repository from component label: rhtpa-server (mapped via pscomponent:org/rhtpa-server)
- Source Repositories table lookup: rhtpa-backend found at https://github.com/rhtpa/rhtpa-backend
- Deployment context: upstream (default -- no Deployment Context column present)
