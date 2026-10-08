# Step 1 -- Data Extraction

## CVE Data Table

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
| Upstream fix PR | (none in remote links) |
| Advisory URL | (none beyond CVE record) |
| Due date | 2026-08-01 |
| Existing comments | (no comments) |
| Status | New |
| Assignee | Unassigned |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Triage scope: 2.2.x stream only (scoped issue)

## Ecosystem Detection

- Ecosystem: **Cargo** (criterion is a Rust crate)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "criterion"'`
- Upstream branch: `release/0.4.z`
- Category: Source dependency
- Remediation tasks per stream: 2 (dependency bump + downstream propagation)
