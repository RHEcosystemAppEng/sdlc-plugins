# Step 1 -- Data Extraction

## Issue: TC-8001

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description |
| Affected version range | < 0.11.14 (versions before 0.11.14) | Description |
| Fixed version | 0.11.14 | Description |
| CVSS | 7.5 (High) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Assignee | Unassigned | Issue field |
| Status | New | Issue field |
| Existing comments | (none) | Issue comments |

## Stream Scope Resolution

The summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration Version Streams table:

| Stream | Konflux Release Repo | Match |
|--------|----------------------|-------|
| 2.1.x | rhtpa-release.0.3.z | No |
| 2.2.x | rhtpa-release.0.4.z | Yes -- matches `rhtpa-2.2` |

**Issue stream scope**: 2.2.x (scoped issue -- Steps 3-4 apply only to this stream)

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. This maps to the **Cargo** ecosystem, which is listed in both streams' Ecosystem Mappings tables:

| Ecosystem | Repository | Lock File | Check Command |
|-----------|------------|-----------|---------------|
| Cargo | backend | Cargo.lock | `git show <tag>:Cargo.lock` |

**Detected ecosystem**: Cargo (Rust crate)

## Deployment Context Lookup

The affected component label `pscomponent:org/rhtpa-server` maps to the **rhtpa-backend** source repository. From the Source Repositories table:

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | upstream (default -- no Deployment Context column) |

**Deployment context**: upstream

## Affects Versions Discrepancy (noted for Step 3)

The PSIRT-assigned Affects Versions field is **RHTPA 2.0.0**, but no 2.0.x stream exists in the Security Configuration. The configured streams are 2.1.x and 2.2.x. This mismatch will need correction in Step 3 after version impact analysis confirms which versions are actually affected.

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |

## Vulnerability Summary

quinn-proto (before version 0.11.14) allows a remote attacker to cause a denial of service by sending a QUIC transport frame that creates an excessive number of streams. The vulnerability is caused by missing validation of the stream count in STREAMS frames, leading to unbounded allocation and a subsequent panic. The fix is in version 0.11.14 (upstream PR: quinn-rs/quinn#2048).
