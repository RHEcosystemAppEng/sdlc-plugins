# Step 1 -- Data Extraction: TC-8050

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99001 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | criterion |
| Affected version range | versions before 0.5.2 |
| Fixed version | 0.5.2 |
| CVSS | 5.3 (Medium) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99001 |
| Upstream fix PR | (none) |
| Advisory URL | (none) |
| Due date | 2026-08-01 |
| Existing comments | (none) |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Konflux release repo: git.example.com/rhtpa/rhtpa-release.0.4.z
- Issue is **scoped** to the 2.2.x stream only

## Ecosystem Detection

- Library: criterion (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`
