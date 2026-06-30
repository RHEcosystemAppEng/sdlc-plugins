# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Reporter | psirt-analyst (account ID: 557058:psirt-analyst-mock-id) |
| Existing comments | None |
| Ecosystem | Cargo (Rust crate) |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the configured Version Stream **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`). This issue is scoped to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate (Cargo ecosystem). Per the Ecosystem Mappings table for the 2.2.x stream, the lock file is `Cargo.lock` and the check command is `git show <tag>:Cargo.lock`. The upstream branch is `release/0.4.z`, and the repository is `backend`.

## Notes

- The PSIRT-assigned Affects Versions (`RHTPA 2.0.0`) does not match any configured version stream. There is no 2.0.x stream in the Version Streams table. This will be corrected in Step 3.
- The issue status is **New**, proceeding with full triage.
