# Step 1 -- Data Extraction

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
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

This issue is **scoped** to the 2.2.x stream. Steps 3 and 4 will operate within this stream's scope only. Cross-stream impact on 2.1.x will be handled via Case B (Step 8).

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The ecosystem is **Cargo**, which is configured in both streams' Ecosystem Mappings tables:

- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch (2.1.x): `release/0.3.z`
- Upstream Branch (2.2.x): `release/0.4.z`

## Deployment Context

The affected repository `rhtpa-backend` is found in the Source Repositories table. No Deployment Context column is present in the configuration (backward compatibility), so the default deployment context is `upstream`.

## Vulnerability Details

A vulnerability was found in quinn-proto. The quinn-proto crate before version 0.11.14 allows a remote attacker to cause a panic by sending a QUIC transport frame that creates an excessive number of streams. This vulnerability is classified as a denial of service (DoS). The vulnerability exists because quinn-proto does not properly validate the number of streams requested in a STREAMS frame. An attacker can send a specially crafted frame that causes the server to allocate an unbounded number of stream state objects, leading to a panic when the allocation exceeds internal limits.

### References

- https://github.com/advisories/GHSA-2026-qp73-x4mq
- https://rustsec.org/advisories/RUSTSEC-2026-0042.html
