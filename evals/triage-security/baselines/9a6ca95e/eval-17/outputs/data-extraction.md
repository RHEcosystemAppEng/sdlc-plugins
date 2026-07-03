# Step 1 -- Data Extraction

## Parsed CVE Data for TC-8001

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Stream scope | 2.2.x (mapped from `[rhtpa-2.2]` to Version Streams table) |
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
| Assignee | Unassigned |
| Status | New |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams table (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`). This issue is **stream-scoped** to 2.2.x -- Steps 3-4 apply only to this stream.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The ecosystem is **Cargo**, which is listed in both streams' Ecosystem Mappings tables. The lock file is `Cargo.lock` and the check command is `git show <tag>:Cargo.lock`.

## Affects Versions Mismatch (Preliminary)

The Jira Affects Versions field currently lists **RHTPA 2.0.0**, but no 2.0.x stream is configured in the Version Streams table. This version does not match any supported stream and will need correction in Step 3 after the version impact analysis determines the actual affected versions.

## Deployment Context

The source repository `rhtpa-backend` does not have a Deployment Context column in the Source Repositories table (backward compatibility). Default deployment context: **upstream**.

## Vulnerability Description

A vulnerability was found in quinn-proto. The quinn-proto crate before version 0.11.14 allows a remote attacker to cause a panic by sending a QUIC transport frame that creates an excessive number of streams. This vulnerability is classified as a denial of service (DoS). The vulnerability exists because quinn-proto does not properly validate the number of streams requested in a STREAMS frame, leading to unbounded allocation of stream state objects and eventual panic.
