# Step 1 -- Data Extraction: TC-8002

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-28940 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | serde_json |
| Affected version range | versions before 1.0.135 |
| Fixed version | 1.0.135 |
| CVSS | 5.3 (Medium) |
| Upstream fix PR | N/A (none in remote links) |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| Due date | 2026-07-30 |
| Existing comments | None |
| Issue status | New |
| Assignee | Unassigned |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`). This issue is **stream-scoped** to 2.2.x.

However, since all streams must be checked for version impact analysis (Step 2), both the 2.1.x and 2.2.x streams are analyzed. Steps 3 and 8 are scoped to the 2.2.x stream only.

## Ecosystem Detection

- **Ecosystem**: Cargo (Rust crate -- serde_json is a Rust serialization library)
- **Category**: Source dependency
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock | grep -A2 'name = "serde_json"'`

## Deployment Context

The affected repository (rhtpa-backend) has no explicit Deployment Context column in the Source Repositories table. Per the skill's backward compatibility rule, the deployment context defaults to `upstream`.

## References

- GitHub Advisory: https://github.com/advisories/GHSA-2026-j9r2-m5vk
- CVE Record: https://www.cve.org/CVERecord?id=CVE-2026-28940
- RustSec Advisory: https://rustsec.org/advisories/RUSTSEC-2026-0019.html
