# Step 1 -- Data Extraction

## Issue: TC-8020

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable library | tokio |
| Affected version range | versions before 1.42.0 |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Upstream fix PR | [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) |
| Advisory URL | [GHSA-2026-tk91-v5pp](https://github.com/advisories/GHSA-2026-tk91-v5pp) |
| CVE record URL | [CVE-2026-55123](https://www.cve.org/CVERecord?id=CVE-2026-55123) |
| Due date | 2026-08-15 |
| Existing comments | None |
| Upstream Affected Component | tokio (customfield_10632) |
| PS Component | pscomponent:org/rhtpa-server (customfield_10669) |
| Stream | rhtpa-2.2 (customfield_10832) |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`).

This is a **scoped** issue -- Steps 3-8 apply to the rhtpa-2.2 stream only. Cross-stream impact for other streams is handled via Case A.

## Ecosystem Detection

- **Library**: tokio (Rust crate)
- **Ecosystem**: Cargo
- **Category**: Source dependency
- **Remediation tasks per stream**: 2 (upstream backport + downstream propagation)
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`

## Deployment Context

The Source Repositories table does not include a Deployment Context column. All repositories default to `upstream`. Coordination guidance subsection is omitted per backward compatibility rules.

## Additional References

- [RUSTSEC-2026-0088](https://rustsec.org/advisories/RUSTSEC-2026-0088.html)
