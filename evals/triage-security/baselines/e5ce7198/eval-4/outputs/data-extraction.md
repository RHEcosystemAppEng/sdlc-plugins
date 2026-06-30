# Data Extraction -- TC-8004

## Step 0 -- Configuration Validation

Configuration extracted from CLAUDE.md:

| Parameter | Value |
|-----------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |

## Step 1 -- Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-33501 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | _(none -- no stream suffix in summary)_ |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | versions before 0.4.8 (< 0.4.8) |
| Fixed version | 0.4.8 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/812 |
| Advisory URL | https://github.com/advisories/GHSA-2026-kv8p-r3n7 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-33501 |
| Due date | 2026-08-01 |
| Existing comments | _(none)_ |
| Status | New |
| Assignee | Unassigned |

### Stream Scope Resolution

The issue summary "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames" has **no stream suffix** in brackets. Therefore this issue is **unscoped** -- it covers all configured version streams (2.1.x and 2.2.x). Steps 3 and 4 will apply across all streams.

### Ecosystem Detection

The vulnerable library is **h2**, a Rust crate. Both stream security matrices configure a Cargo ecosystem with:
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`

Ecosystem: **Cargo** (source dependency)

### Step 1.7 -- Embargo Check

CVE-2026-33501 has CVSS 7.5 (High severity), which meets the embargo check threshold (>= 7.0). However, no Embargo policy URL is configured in the Security Configuration, so this step is **skipped**.
