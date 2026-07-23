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
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | (none) |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`)
- This issue is **scoped** to the 2.2.x stream only

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`

## Deployment Context

- Repository: rhtpa-backend
- Deployment context: **upstream** (default -- no Deployment Context column in Source Repositories table)

## Vulnerability Description

A vulnerability was found in quinn-proto. The quinn-proto crate before version 0.11.14
allows a remote attacker to cause a panic by sending a QUIC transport frame that creates
an excessive number of streams. This vulnerability is classified as a denial of service
(DoS). quinn-proto does not properly validate the number of streams requested in a
STREAMS frame, leading to unbounded allocation and a panic.

## PSIRT Affects Versions Note

The PSIRT-assigned Affects Versions value `RHTPA 2.0.0` does not match any configured
version stream (no 2.0.x stream exists). This will need correction in Step 3 based on
lock file evidence from the version impact analysis.
