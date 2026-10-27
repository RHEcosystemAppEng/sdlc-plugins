# Step 1 -- Data Extraction

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
| Existing comments | None |
| Ecosystem | Cargo |
| Reporter | psirt-analyst (557058:psirt-analyst-mock-id) |

## Stream Scope Resolution

The issue summary contains suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream
(Konflux release repo: `rhtpa-release.0.4.z`). This issue is scoped to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The Ecosystem Mappings table for both
streams lists **Cargo** as the ecosystem with lock file `Cargo.lock` and check command
`git show <tag>:Cargo.lock`.

Ecosystem classification: **Source dependency** -- produces 2 remediation tasks per affected
stream (upstream backport or dependency bump + downstream propagation).
