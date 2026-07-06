# Data Extraction (Step 1) -- TC-8020

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Issue Key | TC-8020 |
| Issue Type | Vulnerability |
| Status | New |
| Affected Component | pscomponent:org/rhtpa-server |
| Product Version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable Library | quinn-proto |
| Affected Version Range | versions before 0.11.14 (< 0.11.14) |
| Fixed Version | 0.11.14 |
| CVSS | 7.5 (High) |
| Due Date | 2026-07-15 |
| Assignee | Unassigned |
| Upstream Affected Component (customfield_10632) | quinn-proto |

## Remote Links

| Type | URL | Description |
|------|-----|-------------|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-qp73-x4mq | GHSA-2026-qp73-x4mq |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-31812 | CVE-2026-31812 |
| Upstream Fix PR | https://github.com/quinn-rs/quinn/pull/2048 | quinn-rs/quinn#2048 |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`). This issue is **stream-scoped** to 2.2.x only. Steps 3 and 4 will apply only to 2.2.x versions.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. Per the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, the ecosystem is **Cargo**. The lock file to inspect is `Cargo.lock` at the pinned backend tag, using the check command `git show <tag>:Cargo.lock`.

As a source dependency ecosystem, remediation will require two tasks per affected stream: an upstream backport task (fix in the source repo) and a downstream propagation subtask (update the reference in the Konflux release repo).

## Version Impact Analysis Summary

### Stream 2.2.x (in scope)

| Product Version | Build Tag | quinn-proto Version | Affected? |
|-----------------|-----------|---------------------|-----------|
| RHTPA 2.2.0 | v0.4.5 | 0.11.9 | YES (< 0.11.14) |
| RHTPA 2.2.1 | v0.4.8 | 0.11.12 | YES (< 0.11.14) |
| RHTPA 2.2.2 | v0.4.9 | 0.11.12 (retag of v0.4.8) | YES (same as 2.2.1) |
| RHTPA 2.2.3 | v0.4.11 | 0.11.14 | NO (>= 0.11.14, fixed) |
| RHTPA 2.2.4 | v0.4.12 | 0.11.14 | NO (>= 0.11.14, fixed) |

### Stream 2.1.x (out of scope, cross-stream analysis)

| Product Version | Build Tag | quinn-proto Version | Affected? |
|-----------------|-----------|---------------------|-----------|
| RHTPA 2.1.0 | v0.3.8 | 0.11.9 | YES (< 0.11.14) |
| RHTPA 2.1.1 | v0.3.12 | 0.11.9 | YES (< 0.11.14) |

## Vulnerability Description

quinn-proto before version 0.11.14 allows a remote attacker to cause a panic by sending a QUIC transport frame that creates an excessive number of streams. This is classified as a denial of service (DoS). The vulnerability exists because quinn-proto does not properly validate the number of streams requested in a STREAMS frame, leading to unbounded allocation and eventual panic.
