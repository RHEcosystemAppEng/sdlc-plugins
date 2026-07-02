# Step 1 -- Data Extraction

## Issue: TC-8001

Parsed from Jira Vulnerability issue TC-8001.

## Extracted CVE Data

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
| Due date | 2026-07-15 |
| Assignee | Unassigned |
| Status | New |
| Existing comments | None |

## Remote Links

| Link | Type |
|------|------|
| [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) | GitHub Advisory |
| [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) | CVE Record |
| [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) | Upstream fix PR |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (Konflux release repo: rhtpa-release.0.4.z)
- This issue is **stream-scoped** to the 2.2.x stream only.

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Detected ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
- Upstream branch: `release/0.4.z` (for the 2.2.x stream)
- Source repository: backend

## Deployment Context

- Repository: rhtpa-backend
- Deployment context: **upstream** (default -- no Deployment Context column in Source Repositories table)

## Vulnerability Summary

quinn-proto (Rust crate) before version 0.11.14 allows a remote attacker to cause a denial of service (DoS) by sending a QUIC transport frame that creates an excessive number of streams. The vulnerability exists because quinn-proto does not properly validate the number of streams requested in a STREAMS frame, leading to unbounded allocation and subsequent panic.

## Notes

- The PSIRT-assigned Affects Versions (RHTPA 2.0.0) does not match any configured version stream (2.1.x or 2.2.x). This will need correction in Step 3 based on lock file evidence from Step 2.
- The issue is scoped to the 2.2.x stream per the summary suffix, but cross-stream impact on 2.1.x should be assessed in Step 2 (Case B analysis).
