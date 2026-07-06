# Step 1 -- Data Extraction

## Issue: TC-8001

## Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels (`CVE-2026-31812`), Summary |
| Affected component | `pscomponent:org/rhtpa-server` | Labels (matches component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description ("A vulnerability was found in quinn-proto") |
| Affected version range | versions before 0.11.14 | Description ("quinn-proto crate before version 0.11.14") |
| Fixed version | 0.11.14 | Description ("Fixed version: 0.11.14") |
| CVSS score | 7.5 (High) | Description ("CVSS: 7.5 (High)") |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) | Remote Links |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) | Remote Links |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) | Remote Links |
| Due date | 2026-07-15 | Jira `duedate` field |
| Existing comments | None | Issue comment history |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration's Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

This issue is **stream-scoped** to the 2.2.x stream. Steps 3 and 4 will apply only to this stream. However, Step 2 (Version Impact Analysis) still checks all streams to detect cross-stream impact (Case B).

## Ecosystem Detection

| Property | Value |
|----------|-------|
| Ecosystem | Cargo |
| Rationale | quinn-proto is a Rust crate; the Ecosystem Mappings table in security-matrix.md lists Cargo for the backend repository |
| Lock file | `Cargo.lock` |
| Check command | `git show <tag>:Cargo.lock` |
| Source repository | backend |
| Upstream branch (2.1.x) | `release/0.3.z` |
| Upstream branch (2.2.x) | `release/0.4.z` |

## Deployment Context

The affected component label `pscomponent:org/rhtpa-server` was looked up in the Source Repositories table. The Source Repositories table lists `rhtpa-backend` as the only source repository. Since the component label does not exactly match a repository name in the table, the deployment context defaults to `upstream`.

## Affects Versions Discrepancy (Noted)

The Jira Affects Versions field is set to **RHTPA 2.0.0**, but the issue summary suffix indicates **rhtpa-2.2** (the 2.2.x stream). There is no 2.0.x stream configured in the Version Streams table. This discrepancy will be addressed in Step 3 (Affects Versions Correction) after the version impact analysis in Step 2 determines which versions actually ship the vulnerable dependency.

## Vulnerability Summary

quinn-proto (a Rust QUIC protocol implementation crate) before version 0.11.14 allows a remote attacker to cause a denial of service (DoS) by sending a QUIC transport frame that creates an excessive number of streams. The server panics when the allocation exceeds internal limits. The fix is available in quinn-proto 0.11.14.
