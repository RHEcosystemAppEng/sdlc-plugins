# Step 1 -- Data Extraction

## Issue: TC-8001

Fetched via `jira.get_issue("TC-8001")` and `jira.get_issue_remote_links("TC-8001")`.

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels (`CVE-2026-31812`) and summary text |
| Affected component | `pscomponent:org/rhtpa-server` | Labels (matches Component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links (quinn-rs/quinn#2048) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links (GitHub Advisory) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links (CVE Record) |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | _(none)_ | Issue comment history |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`.

1. Parsed suffix: `rhtpa-2.2` maps to stream `2.2.x`
2. Matched to Version Streams table: stream `2.2.x` is configured with Konflux Release Repo `git.example.com/rhtpa/rhtpa-release.0.4.z`
3. **Issue stream scope**: `2.2.x` (scoped issue -- Steps 3-7 apply only to this stream's versions)

## Ecosystem Detection

The vulnerable library is `quinn-proto`, which is a Rust crate. This maps to the **Cargo** ecosystem as configured in the stream's security-matrix.md Ecosystem Mappings table.

- **Ecosystem**: Cargo
- **Lock File**: `Cargo.lock`
- **Check Command**: `git show <tag>:Cargo.lock`
- **Upstream Branch**: `release/0.4.z` (for the 2.2.x stream)
- **Source Repository**: backend (rhtpa-backend)

Since this is a source dependency ecosystem (Cargo), remediation will require **two tasks**: an upstream backport task (fix in the source repo) and a downstream propagation subtask (update the reference in the Konflux release repo).
