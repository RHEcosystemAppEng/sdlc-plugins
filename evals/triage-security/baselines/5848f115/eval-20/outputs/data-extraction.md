# Step 1 -- Data Extraction

## Source Issue

- **Jira Key**: TC-8001
- **Issue Type**: Vulnerability
- **Status**: New

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels (`CVE-2026-31812`) and summary text |
| Affected component | `pscomponent:org/rhtpa-server` | Labels (matches component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text ("A vulnerability was found in quinn-proto") |
| Affected version range | < 0.11.14 (versions before 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS score | 7.5 (High) | Description text |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) | Remote links |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) | Remote links |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) | Remote links |
| Due date | 2026-07-15 | Jira `duedate` field |
| Assignee | Unassigned | Jira `assignee` field |
| Existing comments | None | Issue comment history |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`.

- Parsed suffix: `rhtpa-2.2` maps to stream **2.2.x**
- Matched Version Stream: **2.2.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`)
- Issue stream scope: **Scoped to 2.2.x only**

This is a scoped issue. Steps 3 and 4 will apply to the 2.2.x stream, and Case A
cross-stream impact analysis will check whether the 2.1.x stream is also affected.

## Ecosystem Detection

- **Library**: quinn-proto (Rust crate)
- **Ecosystem**: Cargo
- **Category**: Source dependency
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`
- **Upstream branch (2.2.x stream)**: `release/0.4.z`
- **Remediation tasks per stream**: 2 (upstream backport + downstream propagation)

## Deployment Context

- **Affected repository**: rhtpa-backend (matched from component label `pscomponent:org/rhtpa-server`)
- **URL**: https://github.com/rhtpa/rhtpa-backend
- **Deployment context**: upstream (default -- no Deployment Context column in Source Repositories table)

## Affects Versions Discrepancy (Preliminary)

The PSIRT-assigned Affects Versions field shows **RHTPA 2.0.0**, but:

- The issue summary suffix targets stream **2.2.x** (not 2.0.x)
- There is no 2.0.x version stream configured in the Security Configuration
- The configured streams are 2.1.x and 2.2.x

This discrepancy will be corrected in Step 3 (Affects Versions Correction) after
the version impact analysis in Step 2 determines which versions actually ship
the vulnerable dependency.

## Vulnerability Details

quinn-proto (Rust crate) versions before 0.11.14 are vulnerable to a denial of
service (DoS) attack. The vulnerability exists because quinn-proto does not properly
validate the number of streams requested in a QUIC STREAMS frame. An attacker can
send a specially crafted frame that causes the server to allocate an unbounded number
of stream state objects, leading to a panic when the allocation exceeds internal limits.

The fix is available in quinn-proto version 0.11.14 (upstream PR: quinn-rs/quinn#2048).

## References

- GitHub Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq
- RustSec Advisory: https://rustsec.org/advisories/RUSTSEC-2026-0042.html
- CVE Record: https://www.cve.org/CVERecord?id=CVE-2026-31812

## Quinn-proto Version Impact (from Mock Lock File Data)

For reference, the following quinn-proto versions are pinned at each release tag
(data from the security matrix mock lock file section):

| Tag | Product Version | Stream | quinn-proto version | Vulnerable (< 0.11.14)? |
|-----|-----------------|--------|---------------------|------------------------|
| `v0.3.8` | 2.1.0 | 2.1.x | 0.11.9 | YES |
| `v0.3.12` | 2.1.1 | 2.1.x | 0.11.9 | YES |
| `v0.4.5` | 2.2.0 | 2.2.x | 0.11.9 | YES |
| `v0.4.8` | 2.2.1 | 2.2.x | 0.11.12 | YES |
| `v0.4.9` | 2.2.2 | 2.2.x | (same as v0.4.8) | YES (retag of 2.2.1) |
| `v0.4.11` | 2.2.3 | 2.2.x | 0.11.14 | NO (fixed) |
| `v0.4.12` | 2.2.4 | 2.2.x | 0.11.14 | NO (fixed) |

This data is included here for completeness but would formally be produced in Step 2
(Version Impact Analysis). It shows that:

- **2.1.x stream**: All versions (2.1.0, 2.1.1) ship vulnerable quinn-proto (0.11.9 < 0.11.14) -- AFFECTED
- **2.2.x stream**: Versions 2.2.0 through 2.2.2 are affected; versions 2.2.3+ ship the fix (0.11.14) -- PARTIALLY AFFECTED (fixed in 2.2.3)
