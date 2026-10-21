# Step 1 -- Data Extraction: TC-8001

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS Score | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |
| Issue status | New |
| Assignee | Unassigned |

## Stream Scope Resolution

The issue summary contains a stream suffix: `[rhtpa-2.2]`

- Parsed suffix: `rhtpa-2.2` maps to stream **2.2.x**
- Matched Version Stream: **2.2.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`)
- Issue stream scope: **2.2.x** (scoped issue -- Steps 3-8 are scoped to this stream)

## Ecosystem Detection

- Vulnerable library: **quinn-proto** (Rust crate)
- Ecosystem: **Cargo** (source dependency)
- Classification: Source dependency ecosystem -- produces 2 remediation tasks per stream (upstream backport or dependency bump + downstream propagation)

## Deployment Context

- Affected repository: rhtpa-backend
- Deployment context: **upstream** (default -- no Deployment Context column present in Source Repositories table)

## Vulnerability Description

A vulnerability was found in quinn-proto. The quinn-proto crate before version 0.11.14 allows a remote attacker to cause a panic by sending a QUIC transport frame that creates an excessive number of streams. This vulnerability is classified as a denial of service (DoS).

The vulnerability exists because quinn-proto does not properly validate the number of streams requested in a STREAMS frame. An attacker can send a specially crafted frame that causes the server to allocate an unbounded number of stream state objects, leading to a panic when the allocation exceeds internal limits.

## Notes

- The PSIRT-assigned Affects Versions field shows **RHTPA 2.0.0**, which does not correspond to any version in the configured Version Streams (2.1.x and 2.2.x). This will need correction in Step 3 after version impact analysis.
- The issue is scoped to the 2.2.x stream, but cross-stream impact on 2.1.x will be evaluated in Step 2.
