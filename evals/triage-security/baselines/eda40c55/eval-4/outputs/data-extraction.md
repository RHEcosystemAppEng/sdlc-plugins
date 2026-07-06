# Step 1 -- Data Extraction

## Issue Metadata

| Field | Value |
|-------|-------|
| Issue Key | TC-8004 |
| Summary | CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames |
| Issue Type | Vulnerability |
| Status | New |
| Assignee | Unassigned |
| Due Date | 2026-08-01 |

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-33501 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | _(no stream suffix -- unscoped)_ |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | versions before 0.4.8 |
| Fixed version | 0.4.8 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [hyperium/h2#812](https://github.com/hyperium/h2/pull/812) |
| Advisory URL | [GHSA-2026-kv8p-r3n7](https://github.com/advisories/GHSA-2026-kv8p-r3n7) |
| CVE record URL | [CVE-2026-33501](https://www.cve.org/CVERecord?id=CVE-2026-33501) |
| Existing comments | _(none)_ |

## Stream Scope Resolution

The issue summary "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames"
contains **no stream suffix** in brackets. The issue is therefore **unscoped** --
all configured version streams must be analyzed:

- Stream 2.1.x (rhtpa-release.0.3.z)
- Stream 2.2.x (rhtpa-release.0.4.z)

## Ecosystem Detection

The vulnerable library `h2` is a Rust crate. Both streams' Ecosystem Mappings
tables include a **Cargo** ecosystem entry:

| Stream | Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|--------|-----------|------------|-----------|---------------|-----------------|
| 2.1.x | Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| 2.2.x | Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

Ecosystem: **Cargo** (source dependency -- remediation produces 2 tasks per affected stream)

## Deployment Context

Source repository `rhtpa-backend` has no Deployment Context column in the
Source Repositories table. Defaulting to: **upstream**.

## Configuration Validated (Step 0)

| Config Item | Value |
|-------------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Embargo policy URL | _(not configured -- Step 1.7 skipped)_ |
| Upstream Affected Component field | _(not configured -- Steps 4.3 and 7 skipped)_ |
| ProdSec Jira account ID | _(not configured -- @mentions skipped)_ |

## Matrix Staleness Check (Step 0.3)

Both security-matrix.md files contain a `Last-Updated: 2026-06-28T10:00:00Z`
timestamp. As of the current date (2026-07-06), this is 8 days ago, which is
within the 14-day staleness threshold. Proceeding without warning.
