# Step 1 -- Data Extraction

## Issue: TC-8001

## Parsed CVE Data Table

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comment history |
| Status | New | Issue status |
| Assignee | Unassigned | Issue assignee |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped to stream: **2.2.x** (from Version Streams table in Security Configuration)
- Issue stream scope: **scoped to 2.2.x only**

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo** (source dependency)
- Remediation tasks per stream: **2** (upstream backport + downstream propagation)

## Deployment Context

- Repository: rhtpa-backend (matched from component label `pscomponent:org/rhtpa-server`)
- Deployment context: **upstream** (default -- no Deployment Context column in Source Repositories table)

## Additional References

- RUSTSEC advisory: https://rustsec.org/advisories/RUSTSEC-2026-0042.html
- GitHub Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq
