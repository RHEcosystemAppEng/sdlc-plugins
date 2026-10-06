# Step 1 -- Data Extraction

## Issue: TC-8001

**Source**: Jira Vulnerability issue TC-8001

## Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels (`CVE-2026-31812`), summary text |
| Affected component | `pscomponent:org/rhtpa-server` | Labels (matches component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text ("A vulnerability was found in quinn-proto") |
| Affected version range | < 0.11.14 (versions before 0.11.14) | Description text ("before version 0.11.14") |
| Fixed version | 0.11.14 | Description text ("Fixed version: 0.11.14") |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links (quinn-rs/quinn#2048) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links (GitHub Advisory) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links (CVE Record) |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comment history |

## Stream Scope Resolution

- **Summary suffix**: `[rhtpa-2.2]`
- **Mapped stream**: 2.2.x
- **Match**: Confirmed -- `2.2.x` exists in the Version Streams table (Konflux release repo `rhtpa-release.0.4.z`)
- **Issue stream scope**: Scoped to stream **2.2.x** only

This is a **scoped** issue. Steps 3-4 will apply to the 2.2.x stream. Cross-stream
impact on 2.1.x will be evaluated in Step 2 and handled via Case A (cross-stream
impact) if that stream is also affected.

## Affects Versions Mismatch (Preliminary)

The PSIRT-assigned Affects Versions is **RHTPA 2.0.0**, but no `2.0.x` stream is
configured in the Version Streams table. The configured streams are 2.1.x and 2.2.x.
This mismatch will be corrected in Step 3 after lock file evidence is gathered in
Step 2.

## Ecosystem Detection

- **Library**: quinn-proto (Rust crate)
- **Ecosystem**: Cargo
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`
- **Category**: Source dependency
- **Remediation tasks per stream**: 2 (upstream backport + downstream propagation)

The Cargo ecosystem is confirmed in both the 2.1.x and 2.2.x stream Ecosystem
Mappings tables.

## Deployment Context

- **Repository**: rhtpa-backend
- **Deployment context**: upstream (default -- no Deployment Context column in Source Repositories table)

## Vulnerability Summary

quinn-proto (Rust crate) before version 0.11.14 allows a remote attacker to cause
a denial of service (DoS) by sending a QUIC transport frame that creates an excessive
number of streams, leading to a panic. The fix is available in quinn-proto 0.11.14.
CVSS score is 7.5 (High severity).
