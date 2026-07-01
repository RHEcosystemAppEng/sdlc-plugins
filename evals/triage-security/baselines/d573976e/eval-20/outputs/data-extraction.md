# Step 1 -- Data Extraction

## Issue: TC-8001

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels (`CVE-2026-31812`) and summary text |
| Affected component | pscomponent:org/rhtpa-server | Label matching pattern `pscomponent:` |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | < 0.11.14 | Description: "versions before 0.11.14" |
| Fixed version | 0.11.14 | Description: "Fixed version: 0.11.14" |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links (quinn-rs/quinn#2048) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links (GHSA) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links (cve.org) |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comment history |
| Issue status | New | Jira `status` field |
| Reporter | _(not specified in fixture)_ | Issue `reporter` field |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`:

1. Parsed suffix: `rhtpa-2.2` maps to stream `2.2.x`
2. Matched to Version Streams table: stream `2.2.x` is configured with Konflux Release Repo `git.example.com/rhtpa/rhtpa-release.0.4.z`
3. **Issue stream scope**: `2.2.x` -- triage is scoped to the 2.2.x stream only

## Ecosystem Detection

The vulnerable library is `quinn-proto`, which is a Rust crate. Checking the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

The library `quinn-proto` is a Rust crate, which maps to the **Cargo** ecosystem. The Cargo ecosystem is listed in the Ecosystem Mappings table, so automated triage can proceed.

- **Ecosystem**: Cargo
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
- **Upstream branch**: `release/0.4.z`
- **Repository**: backend (rhtpa-backend)

## Deployment Context Lookup

The affected repository is identified from the component label `pscomponent:org/rhtpa-server`, which maps to `rhtpa-backend` in the Source Repositories table. The Source Repositories table in the project CLAUDE.md does NOT include a Deployment Context column. Per the skill protocol, when the Deployment Context column is absent (backward compatibility), all repositories default to `upstream`.

- **Affected repository**: rhtpa-backend
- **Deployment context**: upstream (default -- no Deployment Context column present)

## Status-Aware Handling

The issue status is **New**. This is the default path -- proceeding with full triage.
