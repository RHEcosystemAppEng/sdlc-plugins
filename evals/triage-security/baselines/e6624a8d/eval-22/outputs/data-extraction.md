# Step 1 -- Data Extraction: TC-8021

## Step 0 -- Validate Project Configuration

Verified the following sections exist in CLAUDE.md under `# Project Configuration`:

1. **Repository Registry** -- contains rhtpa-backend entry
2. **Jira Configuration** -- Project key: TC, Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
3. **Code Intelligence** -- configured with serena_backend instance
4. **Security Configuration** -- contains Product Lifecycle, Version Streams, and Source Repositories

Extracted configuration values:

| Config Key | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component custom field | customfield_10632 |

## Step 0.7 -- Assign and Transition to Assigned

Before proceeding with data extraction, the following actions would be taken:

1. **Retrieve current user's Jira account ID** via `jira.user_info()`
2. **Assign TC-8021 to the current user** via `jira.edit_issue(TC-8021, assignee=<current-user-account-id>)`
3. **Discover the target transition** via `jira.get_transitions(TC-8021)` -- select the transition whose target status name is "Assigned"
4. **Transition TC-8021 to Assigned** via `jira.transition_issue(TC-8021, <assigned-transition-id>)` -- the issue is currently in "New" status, so the transition proceeds

These actions provide immediate visibility into who is actively triaging the issue and enable Step 7 (Concurrent Triage Detection) to reliably identify active work.

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version / Fix threshold | 0.11.14 |
| CVSS | 7.5 (High) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Due date | 2026-07-15 |
| Existing comments | None |

## Custom Fields

| Custom Field | Field ID | Value |
|---|---|---|
| Upstream Affected Component | customfield_10632 | quinn-proto |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches configured Version Stream in Security Configuration)
- Issue is **stream-scoped** to the 2.2.x stream only

## Ecosystem Detection

- Library: quinn-proto
- Ecosystem: **Cargo** (Rust crate -- identified from the library name and component context)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Category: Source dependency
- Remediation pattern: 2 tasks per stream (upstream backport + downstream propagation)

## Deployment Context Lookup

- Affected repository: rhtpa-backend (from component label pscomponent:org/rhtpa-server)
- Deployment context: **upstream** (default -- no Deployment Context column in Source Repositories table)

## Remote Links

- [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) -- GitHub Advisory
- [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) -- CVE Record
- [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) -- Upstream fix PR

## Version Impact Analysis (Step 2)

Using the security-matrix-mock.md data, the following version impact table was constructed. The issue is scoped to the 2.2.x stream, but all streams are checked per Important Rule 4.

### 2.1.x Stream (rhtpa-release.0.3.z)

| Version | Build Tag | quinn-proto Version | Affected? | Evidence |
|---------|-----------|---------------------|-----------|----------|
| 2.1.0 | v0.3.8 | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |

### 2.2.x Stream (rhtpa-release.0.4.z)

| Version | Build Tag | quinn-proto Version | Affected? | Evidence |
|---------|-----------|---------------------|-----------|----------|
| 2.2.0 | v0.4.5 | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | **YES** | 0.11.12 < 0.11.14 |
| 2.2.2 | v0.4.9 | _(retag of v0.4.8)_ | **YES** | same as 2.2.1 (retag) |
| 2.2.3 | v0.4.11 | 0.11.14 | **NO** | 0.11.14 >= 0.11.14 (fixed version) |
| 2.2.4 | v0.4.12 | 0.11.14 | **NO** | 0.11.14 >= 0.11.14 (fixed version) |

### Summary

- **2.2.x stream (in scope)**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 ship the fix.
- **2.1.x stream (out of scope)**: Both 2.1.0 and 2.1.1 are affected -- cross-stream impact detected.
