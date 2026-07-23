# Step 1 -- Data Extraction

## Issue: TC-8001

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
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Status | New |
| Assignee | Unassigned |
| Existing comments | None |

## Additional References

- RUSTSEC advisory: https://rustsec.org/advisories/RUSTSEC-2026-0042.html

## Stream Scope Resolution

- **Summary suffix**: `[rhtpa-2.2]`
- **Mapped stream**: 2.2.x
- **Issue stream scope**: Scoped to 2.2.x only (rhtpa-release.0.4.z)

The suffix `[rhtpa-2.2]` maps to the configured Version Stream **2.2.x** (Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.4.z). Steps 3 and 4 will be scoped to this stream.

## Ecosystem Detection

- **Vulnerable library**: quinn-proto (a Rust crate)
- **Detected ecosystem**: Cargo
- **Lock file**: `Cargo.lock` (per Ecosystem Mappings in security-matrix.md)
- **Check command**: `git show <tag>:Cargo.lock` (grep for library name)
- **Upstream branch**: `release/0.4.z` (for stream 2.2.x)

The Cargo ecosystem is listed in both streams' Ecosystem Mappings tables -- supported for automated triage.

## Affects Versions Mismatch (Preliminary)

The PSIRT-assigned Affects Versions value is **RHTPA 2.0.0**, but there is no 2.0.x version stream configured. The Version Streams table only contains 2.1.x and 2.2.x. This will need correction in Step 3 based on lock file evidence from Step 2.

## Vulnerability Description

A vulnerability was found in quinn-proto. The quinn-proto crate before version 0.11.14 allows a remote attacker to cause a panic by sending a QUIC transport frame that creates an excessive number of streams. This vulnerability is classified as a denial of service (DoS). The vulnerability exists because quinn-proto does not properly validate the number of streams requested in a STREAMS frame.

## Version Impact Preview (from mock lock file data)

Based on the mock lock file data provided in the security matrix, the following quinn-proto versions are pinned at each tag:

| Product Version | Stream | Build Tag | quinn-proto version | Affected? (< 0.11.14) |
|-----------------|--------|-----------|---------------------|------------------------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES |
| 2.2.2 | 2.2.x | v0.4.9 | (retag of v0.4.8) | YES (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO |

### Summary

- **Affected versions**: 2.1.0, 2.1.1 (stream 2.1.x); 2.2.0, 2.2.1, 2.2.2 (stream 2.2.x)
- **Not affected versions**: 2.2.3, 2.2.4 (stream 2.2.x) -- ship quinn-proto 0.11.14 (fixed version)
- **Issue is scoped to stream 2.2.x**: Affects Versions should be corrected to RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Cross-stream impact**: Stream 2.1.x (versions 2.1.0, 2.1.1) is also affected but outside this issue's scope -- would be reported via Case B cross-stream impact comment
