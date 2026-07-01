# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | (none listed) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams configuration. Triage is scoped to the 2.2.x stream.

## Ecosystem Detection

The vulnerable library **quinn-proto** is a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, this maps to the **Cargo** ecosystem. The lock file is `Cargo.lock` and the check command is `git show <tag>:Cargo.lock`.
