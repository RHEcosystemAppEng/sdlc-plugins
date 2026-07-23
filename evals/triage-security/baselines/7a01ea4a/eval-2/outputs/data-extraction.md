# Data Extraction -- TC-8002

## Step 0 -- Configuration Validation

Configuration extracted from project CLAUDE.md:

| Parameter | Value |
|-----------|-------|
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

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | upstream (default) |

## Step 0.3 -- Matrix Staleness Check

Matrix Last-Updated timestamp: 2026-06-28T10:00:00Z (25 days ago as of 2026-07-23).
This exceeds the 14-day staleness threshold. In a live triage, the engineer would
be warned and asked whether to refresh, proceed, or stop.

For this eval, proceeding with the current matrix data.

## Step 1 -- Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-28940 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | serde_json |
| Affected version range | versions before 1.0.135 |
| Fixed version | 1.0.135 |
| CVSS | 5.3 (Medium) |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| Due date | 2026-07-30 |
| Existing comments | None |
| Issue status | New |
| Assignee | Unassigned |

### Stream Scope Resolution

Summary suffix `[rhtpa-2.2]` maps to stream **2.2.x** in the Version Streams table.
This issue is **scoped** to the 2.2.x stream only.

### Ecosystem Detection

Library `serde_json` is a Rust crate. The ecosystem is **Cargo**.

From the Ecosystem Mappings in the 2.2.x stream's security-matrix.md:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

### Deployment Context

Repository `rhtpa-backend` has no explicit Deployment Context column in the Source
Repositories table. Defaulting to `upstream`.

## Step 1.5 -- External CVE Data Enrichment

In this eval, external APIs (MITRE CVE API, OSV.dev) are not called. Using Jira
description data as the authoritative source:

- **Affected range**: versions before 1.0.135
- **Fix threshold**: 1.0.135

## Step 1.7 -- Embargo Check

CVSS is 5.3 (Medium), which is below the embargo threshold of 7.0. No embargo
policy URL is configured in the Security Configuration. Embargo check skipped.
