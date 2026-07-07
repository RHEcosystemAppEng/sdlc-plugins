# Step 1 -- Data Extraction: TC-8021

## Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 (stream 2.2.x) | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description |
| Affected version range | versions before 0.11.14 | Description |
| Fixed version | 0.11.14 | Description |
| CVSS | 7.5 (High) | Description |
| Upstream fix PR | quinn-rs/quinn#2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comment history |
| Upstream Affected Component (customfield_10632) | quinn-proto | Custom field |

## Stream Scope Resolution

The issue summary contains `[rhtpa-2.2]`, which maps to the **2.2.x** version stream
in the Security Configuration Version Streams table:

- Stream: 2.2.x
- Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.4.z
- Local Path: /home/dev/repos/rhtpa-release.0.4.z

This issue is **stream-scoped** to 2.2.x. Steps 3 and 4 will be scoped to this stream,
and Case B cross-stream analysis will check other streams (2.1.x).

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. Based on the Ecosystem Mappings
table in the 2.2.x stream's security-matrix.md:

- **Ecosystem**: Cargo
- **Repository**: backend
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`
- **Upstream branch**: `release/0.4.z`

Cargo is a source dependency ecosystem, so remediation (if needed) would require
**two tasks**: an upstream backport task (fix in the source repo) and a downstream
propagation subtask (update the reference in the Konflux release repo).

## Deployment Context Lookup

The affected repository `rhtpa-backend` is found in the Source Repositories table:

- URL: https://github.com/rhtpa/rhtpa-backend
- Deployment Context: upstream (default, no explicit column)

## PSIRT Affects Versions Assessment

The PSIRT-assigned Affects Versions value is **RHTPA 2.0.0**. This appears incorrect:
- The Jira version prefix is `RHTPA`
- There is no 2.0.x version stream configured
- The issue is scoped to stream 2.2.x per the summary suffix `[rhtpa-2.2]`
- This will be corrected in Step 3 based on lock file evidence

## Version Impact Analysis (Step 2)

### Stream 2.2.x (issue scope)

| Version | Build | Tag | quinn-proto Version | Affected? | Notes |
|---------|-------|-----|---------------------|-----------|-------|
| 2.2.0 | 0.4.5 | v0.4.5 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.1 | 0.4.8 | v0.4.8 | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.2 | 0.4.9 | v0.4.9 | 0.11.12 | YES | Retag of v0.4.8, same as 2.2.1 |
| 2.2.3 | 0.4.11 | v0.4.11 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4 | 0.4.12 | v0.4.12 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |

The fix was introduced in version 2.2.3 (build 0.4.11). The latest shipped version
(2.2.4) already includes the fix. No new remediation task is needed for the 2.2.x stream.

### Stream 2.1.x (cross-stream analysis for Case B)

| Version | Build | Tag | quinn-proto Version | Affected? | Notes |
|---------|-------|-----|---------------------|-----------|-------|
| 2.1.0 | 0.3.8 | v0.3.8 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.1.1 | 0.3.12 | v0.3.12 | 0.11.9 | YES | 0.11.9 < 0.11.14 |

All versions in the 2.1.x stream ship quinn-proto 0.11.9, which is vulnerable.
The latest build (v0.3.12) is still affected. The 2.1.x stream requires remediation.
