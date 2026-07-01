# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable library | tokio |
| Affected version range | < 1.42.0 |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 |
| Advisory URL | https://github.com/advisories/GHSA-2026-tk91-v5pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Due date | 2026-08-15 |
| Existing comments | None |
| Upstream Affected Component | tokio (customfield_10632) |
| PS Component | pscomponent:org/rhtpa-server (customfield_10669) |
| Stream | rhtpa-2.2 (customfield_10832) |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams table.

Issue stream scope: **2.2.x** (rhtpa-2.2)

## Ecosystem Detection

The vulnerable library is **tokio**, a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, the ecosystem is **Cargo**.

- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`
- Repository: backend

This is a source dependency ecosystem, so remediation will follow the two-task pattern (upstream backport + downstream propagation).
