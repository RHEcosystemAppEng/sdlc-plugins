# Step 1 -- Data Extraction: TC-8021

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Issue Key | TC-8021 |
| Issue Type | Vulnerability |
| Status | New |
| Summary | CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.1] |
| Vulnerable library | tokio |
| Affected version range | versions before 1.42.0 |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Affects Versions (PSIRT-claimed) | RHTPA 2.1.0, RHTPA 2.1.1 |
| Due Date | 2026-08-15 |
| Assignee | Unassigned |
| Component label | pscomponent:org/rhtpa-server |
| Upstream Affected Component (customfield_10632) | tokio |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-server |
| Stream (customfield_10832) | rhtpa-2.1 |

## Stream Scope Resolution

- Summary stream suffix: `[rhtpa-2.1]`
- Mapped to configured Version Stream: **2.1.x**
- Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.3.z`
- Local path: `/home/dev/repos/rhtpa-release.0.3.z`
- This is a **scoped** issue -- triage is scoped to the 2.1.x stream only.

## Ecosystem Detection

- Library: tokio (Rust crate)
- Ecosystem: **Cargo**
- Category: Source dependency
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.3.z`
- Expected remediation task count per stream: 2 (upstream backport/dependency bump + downstream propagation)

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-tk91-v5pp |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 |

## Existing Issue Links

No existing links on TC-8021.

## Existing Comments

No comments on TC-8021.
