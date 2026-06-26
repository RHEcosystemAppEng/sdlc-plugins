# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server (from label) |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Stream scope | 2.2.x (maps to Konflux release repo rhtpa-release.0.4.z) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 (quinn-rs/quinn#2048) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Assignee | Unassigned |
| Status | New |
| Existing comments | None |
| Ecosystem | Cargo (Rust crate) |

## Stream Scope Resolution

The summary suffix `[rhtpa-2.2]` maps to stream **2.2.x** in the Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

This issue is **stream-scoped** to 2.2.x only. Steps 3-4 apply to this stream. Cross-stream impact on 2.1.x is handled via Case B (comment only, no Affects Versions changes on the 2.1.x stream from this issue).

## Ecosystem Detection

quinn-proto is a Rust crate. From the Ecosystem Mappings table for the 2.2.x stream:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

This is a **source dependency ecosystem** (Cargo), which means remediation will produce **two tasks**: an upstream backport task and a downstream propagation subtask.

## Affects Versions Discrepancy (noted for Step 3)

The current Affects Versions field shows "RHTPA 2.0.0", but no 2.0.x stream exists in the Version Streams configuration. This will need correction in Step 3 based on the version impact analysis in Step 2.
