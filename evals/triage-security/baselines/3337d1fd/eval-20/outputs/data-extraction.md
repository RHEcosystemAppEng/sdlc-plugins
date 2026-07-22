# Step 1 -- Data Extraction

## Issue: TC-8001

## Parsed CVE Data Table

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels (`CVE-2026-31812`) and summary text |
| Affected component | `pscomponent:org/rhtpa-server` | Labels (matches component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text ("A vulnerability was found in quinn-proto") |
| Affected version range | < 0.11.14 (versions before 0.11.14) | Description text ("before version 0.11.14") |
| Fixed version | 0.11.14 | Description text ("Fixed version: 0.11.14") |
| CVSS score | 7.5 (High) | Description text ("CVSS: 7.5 (High)") |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) | Remote links |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) | Remote links |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | (none) | Issue comment history |

## Stream Scope Resolution

- **Summary suffix**: `[rhtpa-2.2]`
- **Mapped stream**: 2.2.x
- **Matching Version Stream entry**: Stream 2.2.x, Konflux Release Repo `git.example.com/rhtpa/rhtpa-release.0.4.z`, Local Path `/home/dev/repos/rhtpa-release.0.4.z`
- **Issue stream scope**: Scoped to stream 2.2.x only

Since the issue summary contains `[rhtpa-2.2]`, this maps to the `2.2.x` stream in the Version Streams table from Security Configuration. Steps 3-4 will be scoped to this single stream (only 2.2.x versions will be included in Affects Versions correction; other streams are handled via cross-stream companion issue logic in Case B).

## Ecosystem Detection

- **Vulnerable library**: quinn-proto
- **Ecosystem**: Cargo (Rust crate)
- **Rationale**: quinn-proto is a Rust crate (part of the quinn QUIC library). The Ecosystem Mappings table in the security matrix confirms Cargo is a configured ecosystem for both streams.
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`
- **Upstream branches**: `release/0.3.z` (2.1.x stream), `release/0.4.z` (2.2.x stream)

## Deployment Context Lookup

- **Affected repository**: rhtpa-backend (derived from component label `pscomponent:org/rhtpa-server`)
- **Source Repositories match**: rhtpa-backend at `https://github.com/rhtpa/rhtpa-backend`
- **Deployment context**: upstream (default -- no Deployment Context column in Source Repositories table)

## Affects Versions Discrepancy (Preliminary)

The PSIRT-assigned Affects Versions (`RHTPA 2.0.0`) does not correspond to any configured version stream. The configured streams are 2.1.x and 2.2.x. This will need correction in Step 3 after the version impact analysis determines exactly which versions are affected.

## Vulnerability Summary

CVE-2026-31812 is a denial of service (DoS) vulnerability in the quinn-proto Rust crate (versions before 0.11.14). The vulnerability allows a remote attacker to cause a panic by sending a QUIC transport frame that creates an excessive number of streams. The quinn-proto crate does not properly validate the number of streams requested in a STREAMS frame, allowing an attacker to trigger unbounded allocation of stream state objects leading to a panic. The fix is available in quinn-proto version 0.11.14. CVSS score is 7.5 (High severity).

## Critical Field Validation

All critical fields were successfully parsed:

- CVE ID: CVE-2026-31812 -- PRESENT
- Vulnerable library: quinn-proto -- PRESENT
- Affected version range: < 0.11.14 -- PRESENT
- Fixed version: 0.11.14 -- PRESENT

No missing critical fields. Ready to proceed to Step 1.5 (External CVE Data Enrichment).
