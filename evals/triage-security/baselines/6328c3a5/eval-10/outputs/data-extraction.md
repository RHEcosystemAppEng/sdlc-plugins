# Step 1 -- Data Extraction: TC-8020

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Issue Key | TC-8020 |
| Summary | CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected Component | pscomponent:org/rhtpa-server |
| Upstream Affected Component | tokio |
| PS Component | pscomponent:org/rhtpa-server |
| Stream (custom field) | rhtpa-2.2 |
| Vulnerable Library | tokio |
| Affected Version Range | versions before 1.42.0 |
| Fixed Version | 1.42.0 |
| CVSS | 8.1 (High) |
| Affects Versions (PSIRT-claimed) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Due Date | 2026-08-15 |
| Assignee | Unassigned |
| Labels | CVE-2026-55123, pscomponent:org/rhtpa-server |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry for `rhtpa-release.0.4.z`)
- Issue is **scoped** to stream rhtpa-2.2

## Ecosystem Detection

- Library: tokio (Rust crate)
- Ecosystem: **Cargo**
- Classification: **Source dependency** -- 2 remediation tasks per stream (upstream backport or dependency bump + downstream propagation)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-tk91-v5pp |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Upstream Fix PR | https://github.com/tokio-rs/tokio/pull/7001 |

## Additional References

- https://rustsec.org/advisories/RUSTSEC-2026-0088.html

## Deployment Context

- Repository: rhtpa-backend
- Deployment context: upstream (default -- Deployment Context column absent from Source Repositories table)

## Configuration Extracted (Step 0)

| Setting | Value |
|---------|-------|
| Project Key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira Version Prefix | RHTPA |
| Vulnerability Issue Type ID | 10024 |
| Product Pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component Label Pattern | pscomponent: |
| VEX Justification Custom Field | customfield_12345 |
| Upstream Affected Component Field | customfield_10632 |
| PS Component Field | customfield_10669 |
| Stream Field | customfield_10832 |
