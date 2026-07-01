# Step 1 -- Data Extraction

## Issue Details

**Issue Key**: TC-8001
**Summary**: CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**Issue Type**: Vulnerability
**Status**: New

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels (`CVE-2026-31812`), summary text |
| Affected component | pscomponent:org/rhtpa-server | Label matching component label pattern `pscomponent:` |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field (current, PSIRT-assigned) |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | < 0.11.14 | Description text ("versions before 0.11.14") |
| Fixed version | 0.11.14 | Description text ("Fixed version: 0.11.14") |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links (quinn-rs/quinn#2048) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links (GitHub Advisory) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links (CVE Record) |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comment history |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`. This maps to the **2.2.x** stream in the Version Streams table:

- Stream: **2.2.x**
- Konflux Release Repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Local Path: `/home/dev/repos/rhtpa-release.0.4.z`

The issue is **stream-scoped** to 2.2.x. Steps 3-8 will be scoped to this stream only.

## Ecosystem Detection

The vulnerable library is **quinn-proto**, which is a Rust crate. Checking the Ecosystem Mappings table from the 2.2.x stream's `security-matrix.md`:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

The library `quinn-proto` is a Rust crate, matching the **Cargo** ecosystem. This ecosystem is listed in the Ecosystem Mappings table, so automated triage proceeds.

- **Ecosystem**: Cargo
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`
- **Upstream branch**: `release/0.4.z`

## Deployment Context Lookup

The Source Repositories table in the project configuration does **not** include a Deployment Context column. Per backward compatibility rules, all repositories default to `upstream`.

- Repository: rhtpa-backend
- Deployment context: upstream (default -- no Deployment Context column present)
