# Step 1 -- Data Extraction

## Source

Issue: **TC-8001**

## Parsed CVE Data Table

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 (versions before 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Status | New |
| Assignee | Unassigned |
| Existing comments | None |

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |

## Additional References (from description)

- https://rustsec.org/advisories/RUSTSEC-2026-0042.html

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry for 2.2.x at git.example.com/rhtpa/rhtpa-release.0.4.z)
- Issue is **stream-scoped** to the 2.2.x stream
- Steps 3-4 will be scoped to the 2.2.x stream; Case A cross-stream analysis will check 2.1.x for impact

## Ecosystem Detection

- Vulnerable library: quinn-proto (Rust crate)
- Detected ecosystem: **Cargo**
- Category: Source dependency
- Remediation task structure: **2 tasks per affected stream** (upstream backport + downstream propagation)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`

## Affects Versions Mismatch (preliminary)

The PSIRT-assigned Affects Versions field contains **RHTPA 2.0.0**, but the configured Version Streams are **2.1.x** and **2.2.x**. There is no 2.0.x stream in the Security Configuration. This Affects Versions value appears incorrect and will need correction in Step 3 after version impact analysis confirms which versions are actually affected.

## Vulnerability Details

quinn-proto crate before version 0.11.14 allows a remote attacker to cause a panic by sending a QUIC transport frame that creates an excessive number of streams. This is classified as a denial of service (DoS) vulnerability. The vulnerability exists because quinn-proto does not properly validate the number of streams requested in a STREAMS frame. An attacker can send a specially crafted frame that causes the server to allocate an unbounded number of stream state objects, leading to a panic when the allocation exceeds internal limits.
