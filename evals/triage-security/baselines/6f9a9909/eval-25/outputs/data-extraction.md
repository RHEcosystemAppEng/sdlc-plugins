# Step 0 -- Validate Project Configuration

Configuration validated from project CLAUDE.md:

| Config Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories

| Repository | URL | Local Path |
|------------|-----|------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend |

## Step 0.3 -- Matrix Staleness Check

Security matrix `Last-Updated` timestamp: `2026-06-28T10:00:00Z` (100 days ago as of 2026-10-06).

The matrix is older than 14 days and would trigger a staleness warning. For this eval, proceeding with the current matrix.

---

# Step 1 -- Data Extraction

## Parsed CVE Data from TC-8040

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Due date | 2026-07-15 |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Existing comments | None |
| Issue status | New |
| Assignee | Unassigned |

## Stream Scope Resolution

Summary suffix: `[rhtpa-2.2]` maps to configured stream **2.2.x** (Konflux release repo `rhtpa-release.0.4.z`).

Issue is **stream-scoped** to 2.2.x. Steps 3-4 will be scoped to this single stream.

## Ecosystem Detection

Detected ecosystem: **Go modules**

The Ecosystem Mappings tables for both version streams (2.1.x and 2.2.x) list the following supported ecosystems:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` (2.1.x) / `release/0.4.z` (2.2.x) |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

**Go modules is NOT listed in the Ecosystem Mappings table for any configured stream.**

Automated triage cannot proceed for this ecosystem. See `unsupported-ecosystem.md` for the notification.

## Deployment Context Lookup

Repository `rhtpa-backend` found in Source Repositories table. No Deployment Context column present (backward compatibility) -- defaulting to `upstream`.
