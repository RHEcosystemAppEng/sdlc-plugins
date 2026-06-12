# Step 1 - Data Extraction

## Issue: TC-8001

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |
| Status | New |
| Assignee | Unassigned |

## Stream Scope Resolution

The summary suffix `[rhtpa-2.2]` maps to the **2.2.x** version stream, covered by the Konflux release repo `rhtpa-release.0.4.z`. This issue is **stream-scoped** to 2.2.x only.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. Per the Ecosystem Mappings in the 2.2.x stream's security-matrix.md, this falls under the **Cargo** ecosystem:

- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Source repository: backend
- Upstream branch: `release/0.4.z`

## Notes

- The PSIRT-assigned Affects Versions value "RHTPA 2.0.0" does not correspond to any configured version stream (no 2.0.x stream exists). This will need correction in Step 3.
- The vulnerability is a denial of service (DoS) caused by improper validation of stream counts in QUIC transport frames, leading to a panic from unbounded stream state allocation.
