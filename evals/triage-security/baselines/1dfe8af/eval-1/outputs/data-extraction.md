# Step 1 -- Data Extraction

## Parsed CVE Data for TC-8001

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Stream scope | 2.2.x |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | quinn-rs/quinn#2048 (https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |
| Ecosystem | Cargo (Rust crate -- identified from quinn-proto library name and Ecosystem Mappings in security-matrix.md) |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo `rhtpa-release.0.4.z`). This issue is stream-scoped to 2.2.x only. Steps 3 and 7 will be scoped to this stream; cross-stream impact on 2.1.x will be reported via Case B (cross-stream impact comment).

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The Ecosystem Mappings tables in both streams configure a **Cargo** ecosystem with:
- Repository: backend
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.3.z` (2.1.x stream) / `release/0.4.z` (2.2.x stream)

Since this is a source dependency ecosystem (Cargo), remediation will require two tasks: upstream backport + downstream propagation with Blocks dependency.
