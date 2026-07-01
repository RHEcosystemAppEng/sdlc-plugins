# Step 1 -- Data Extraction

## Issue Details

| Field | Value |
|-------|-------|
| **Issue Key** | TC-8004 |
| **Summary** | CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames |
| **Issue Type** | Vulnerability |
| **Status** | New |
| **Due Date** | 2026-08-01 |
| **Assignee** | Unassigned |

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-33501 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (Component label pattern: `pscomponent:`) |
| Product version (PSIRT-claimed) | _(none -- unscoped)_ | No stream suffix in summary |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.2.0 | Jira `versions` field |
| Vulnerable library | h2 | Description text |
| Affected version range | < 0.4.8 | Description: "versions before 0.4.8" |
| Fixed version | 0.4.8 | Description: "Fixed version: 0.4.8" |
| CVSS | 7.5 (High) | Description |
| Upstream fix PR | [hyperium/h2#812](https://github.com/hyperium/h2/pull/812) | Remote links |
| Advisory URL | [GHSA-2026-kv8p-r3n7](https://github.com/advisories/GHSA-2026-kv8p-r3n7) | Remote links |
| CVE record URL | [CVE-2026-33501](https://www.cve.org/CVERecord?id=CVE-2026-33501) | Remote links |
| Due date | 2026-08-01 | Issue `duedate` field |
| Existing comments | _(none)_ | Issue comment history |

## Stream Scope Resolution

The issue summary "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames" has **no stream suffix** in brackets. This issue is treated as **unscoped** -- it covers all configured version streams.

All streams will be analyzed:
- **2.1.x** (Konflux release repo: rhtpa-release.0.3.z)
- **2.2.x** (Konflux release repo: rhtpa-release.0.4.z)

## Ecosystem Detection

The vulnerable library is **h2**, a Rust crate. Based on the Ecosystem Mappings tables in both stream security matrices, this maps to the **Cargo** ecosystem.

- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch (2.1.x): `release/0.3.z`
- Upstream Branch (2.2.x): `release/0.4.z`

Cargo is listed in the Ecosystem Mappings table for both streams -- this is a supported ecosystem.

## Deployment Context Lookup

The Source Repositories table in the project configuration does **not** include a Deployment Context column. Per Step 0 backward compatibility rules, all repositories default to `upstream`. No Coordination Guidance subsection will be added to remediation task descriptions.
