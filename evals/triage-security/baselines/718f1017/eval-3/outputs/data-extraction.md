# Data Extraction — TC-8003

## Step 0 -- Validate Project Configuration

Configuration validated from CLAUDE.md:

| Config Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend (https://github.com/rhtpa/rhtpa-backend) |

All required Security Configuration sections are present: Product Lifecycle, Version Streams, Source Repositories.

## Step 1 -- Extracted Fields

| Field | Value | Source |
|---|---|---|
| CVE ID | CVE-2026-31812 | Labels, summary text |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches Component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | [rhtpa-2.2] | Summary suffix in brackets |
| Affects Versions (Jira field) | RHTPA 2.2.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | N/A (not present in remote links) | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links (GitHub Advisory) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links (CVE Record) |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comment history |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`.

1. Parsed suffix: `[rhtpa-2.2]` -> stream `2.2.x`
2. Matched to configured Version Stream: **2.2.x** (Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.4.z)
3. Issue stream scope: **2.2.x only** (scoped issue)

Steps 3-7 will be scoped to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md:

- **Ecosystem**: Cargo
- **Repository**: backend
- **Lock File**: `Cargo.lock`
- **Check Command**: `git show <tag>:Cargo.lock`
- **Upstream Branch**: `release/0.4.z`

This is a source dependency ecosystem, which means remediation (if needed) would require two tasks: an upstream backport task and a downstream propagation subtask.

## Step 1.5 -- External CVE Data Enrichment

(Simulated -- not calling external APIs per eval constraints)

The Jira description states:
- Affected versions: before 0.11.14
- Fixed version: 0.11.14

These would be cross-validated against MITRE CVE API and OSV.dev in a real triage.

## Step 1.7 -- Embargo Check

CVE-2026-31812 has CVSS 7.5 (High severity), which meets the threshold (>= 7.0).
However, no Embargo policy URL is configured in the Security Configuration, so this step is skipped entirely per the methodology.
