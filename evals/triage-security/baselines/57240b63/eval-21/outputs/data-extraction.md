# Step 1 -- Data Extraction for TC-8020

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches `pscomponent:` pattern from Security Configuration) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | quinn-rs/quinn#2048 | Remote links |
| Advisory URL | GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comments |
| Upstream Affected Component | quinn-proto | customfield_10632 |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams table from Security Configuration:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| **2.2.x** | **git.example.com/rhtpa/rhtpa-release.0.4.z** | **/home/dev/repos/rhtpa-release.0.4.z** |

**Issue stream scope**: 2.2.x

Steps 3 and 4 will be scoped to the 2.2.x stream only. Cross-stream impact on 2.1.x will be reported via Case B in Step 8.

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. The Ecosystem Mappings table in security-matrix.md for stream 2.2.x lists:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| **Cargo** | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

Detected ecosystem: **Cargo** (Rust crate in Cargo.lock).

This means remediation will require **two tasks** per affected stream: an upstream backport task (fix in the source repo) and a downstream propagation subtask (update the Konflux release repo reference).

## Deployment Context Lookup

The affected repository from the component label `pscomponent:org/rhtpa-server` maps to `rhtpa-backend` in the Source Repositories table. The Source Repositories table does not include a Deployment Context column, so the default context of `upstream` applies.

## Version Impact Analysis (Step 2)

Using the mock lock file data from security-matrix.md, dependency versions at each pinned commit:

### Stream 2.2.x (issue scope)

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | **YES** | 0.11.9 < 0.11.14 (fix threshold) |
| 2.2.1 | v0.4.8 | 0.11.12 | **YES** | 0.11.12 < 0.11.14 |
| 2.2.2 | v0.4.9 | 0.11.12 | **YES** | Retag of v0.4.8 -- same as 2.2.1 |
| 2.2.3 | v0.4.11 | 0.11.14 | **NO** | 0.11.14 >= 0.11.14 (at fix threshold) |
| 2.2.4 | v0.4.12 | 0.11.14 | **NO** | 0.11.14 >= 0.11.14 |

### Stream 2.1.x (cross-stream -- out of scope for this issue)

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |

## Affects Versions Assessment

The PSIRT-assigned Affects Versions is `RHTPA 2.0.0`. This is incorrect:

- There is no 2.0.x stream configured in Version Streams.
- The issue is scoped to stream 2.2.x.
- Lock file evidence shows versions RHTPA 2.2.0, 2.2.1, and 2.2.2 are affected.
- Versions RHTPA 2.2.3 and 2.2.4 are NOT affected (ship the fixed quinn-proto 0.11.14).

**PROPOSAL** -- Correct Affects Versions:
- Current: `[RHTPA 2.0.0]`
- Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

This requires engineer confirmation before execution.
