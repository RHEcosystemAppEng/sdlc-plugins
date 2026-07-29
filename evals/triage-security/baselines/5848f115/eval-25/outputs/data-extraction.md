# Step 1 -- Data Extraction: TC-8040 (CVE-2026-31812)

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary text |
| Affected component | pscomponent:org/rhtpa-server | Labels (component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | < 0.11.14 (versions before 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links (quinn-rs/quinn#2048) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links (GHSA-2026-qp73-x4mq) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comment history |
| Status | New | Issue status field |
| Assignee | Unassigned | Issue assignee field |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the configured Version Streams table.

- Parsed suffix: `[rhtpa-2.2]` -> stream `2.2.x`
- Matched stream: 2.2.x (Konflux Release Repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`)
- Issue stream scope: **2.2.x only** (scoped issue)

## Ecosystem Detection

The vulnerable library `quinn-proto` was analyzed in the context of the affected component `pscomponent:org/rhtpa-server`. The ecosystem detection resolved to: **Go modules**.

### Ecosystem Mappings Lookup

The 2.2.x stream's `security-matrix.md` Ecosystem Mappings table lists the following supported ecosystems:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

The 2.1.x stream's `security-matrix.md` Ecosystem Mappings table lists the same supported ecosystems:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

**Result**: The detected ecosystem **Go modules** is NOT listed in the Ecosystem Mappings table for any configured version stream. The supported ecosystems are Cargo and RPM only.

## Deployment Context Lookup

The affected repository `rhtpa-backend` was looked up in the Source Repositories table from CLAUDE.md Security Configuration. No Deployment Context column is present, so the default of `upstream` is applied.

- Repository: rhtpa-backend
- URL: https://github.com/rhtpa/rhtpa-backend
- Deployment context: upstream (default)

## Vulnerability Summary

A denial of service vulnerability in quinn-proto (QUIC transport library) allows a remote attacker to cause a panic by sending a QUIC transport frame that creates an excessive number of streams. The quinn-proto crate before version 0.11.14 does not properly validate the number of streams requested in a STREAMS frame. An attacker can send a specially crafted frame that causes the server to allocate an unbounded number of stream state objects, leading to a panic when the allocation exceeds internal limits.

## Triage Status

**BLOCKED**: Ecosystem detection resolved to "Go modules", which is not listed in any stream's Ecosystem Mappings table. Automated triage cannot proceed. See `unsupported-ecosystem.md` for the notification presented to the user.
