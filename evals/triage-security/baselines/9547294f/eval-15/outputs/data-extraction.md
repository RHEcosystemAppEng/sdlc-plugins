# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] (stream 2.2.x) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Ecosystem | Cargo (Rust crate) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Issue status | New |
| Reporter | psirt-analyst (account ID: 557058:psirt-analyst-mock-id) |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream
in the Version Streams configuration. Triage is scoped to the 2.2.x stream.

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. Based on the Ecosystem Mappings
table in the 2.2.x stream's security-matrix.md, the ecosystem is **Cargo**. The lock file
to inspect is `Cargo.lock` and the check command is `git show <tag>:Cargo.lock`.

As a source dependency ecosystem (Cargo), remediation will follow the two-task pattern:
upstream backport task + downstream propagation subtask.
