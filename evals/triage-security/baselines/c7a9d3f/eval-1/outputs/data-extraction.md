# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data

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

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`).

This issue is **stream-scoped** to 2.2.x. Steps 3-7 will be scoped to this stream only. The 2.1.x stream is outside the scope of this issue but will be analyzed for cross-stream impact (Step 7, Case B).

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. Based on the Ecosystem Mappings table in the security matrix, this falls under the **Cargo** ecosystem:

- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch (2.1.x stream): `release/0.3.z`
- Upstream branch (2.2.x stream): `release/0.4.z`
- Repository: backend

Since this is a source dependency ecosystem (Cargo), remediation will require **two tasks** per affected stream: an upstream backport task and a downstream propagation subtask.

## Additional References

- RustSec advisory: https://rustsec.org/advisories/RUSTSEC-2026-0042.html
- Vulnerability type: Denial of Service (DoS) -- panic caused by excessive stream counts in QUIC transport frames
