# Step 1 – Data Extraction — TC-8001

Source: mock Jira issue `vuln-issue-standard.md`. This stands in for `jira.get_issue` and `jira.get_issue_remote_links`. No Jira calls were made.

## Step 0 Configuration (from claude-md-security-config.md)

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component field | Not configured (so Steps 4.3 and 7 will be skipped) |
| Embargo policy URL | Not configured (so Step 1.7 will be skipped) |
| ProdSec contact / account ID | Not configured |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (https://github.com/rhtpa/rhtpa-backend). No Deployment Context column, so the default is `upstream` |

All required sections are present, so validation passes.

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8001 | Issue key |
| Issue type / Status | Vulnerability / New | Issue fields (status New, so full triage runs) |
| CVE ID | **CVE-2026-31812** | Label `CVE-2026-31812` and summary text (they agree) |
| Affected component | `pscomponent:org/rhtpa-server` (component: `org/rhtpa-server`) | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]`, which maps to stream **2.2.x** | Summary suffix |
| Affects Versions (Jira field) | **RHTPA 2.0.0** | `versions` field |
| Vulnerable library | **quinn-proto** | Description |
| Affected version range | **< 0.11.14** ("versions before 0.11.14") | Description |
| Fixed version | **0.11.14** | Description |
| CVSS / Severity | 7.5 (High), Denial of Service (panic from excessive stream count) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 (quinn-rs/quinn#2048) | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (GHSA-2026-qp73-x4mq). Also: https://rustsec.org/advisories/RUSTSEC-2026-0042.html (description reference) | Remote links / description |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | `duedate` field |
| Assignee | Unassigned | Issue field |
| Existing comments | None | Comment history |

All critical fields (CVE ID, library, affected range) parsed successfully, so there is no need to stop.

## Stream Scope Resolution

| Item | Value |
|------|-------|
| Summary suffix | `[rhtpa-2.2]` |
| Mapped stream | **2.2.x** (matches the configured Version Stream `git.example.com/rhtpa/rhtpa-release.0.4.z`) |
| Issue stream scope | **Scoped to 2.2.x** |

The issue is scoped. Steps 3 and 4 apply to 2.2.x only. If the analysis also finds stream 2.1.x affected, that is handled through Case A (cross-stream / preemptive).

## Affects Versions Observation (handled in Step 3)

The Jira Affects Versions field says **RHTPA 2.0.0**. The summary scopes the issue to stream **2.2.x**, and no 2.0.x stream is configured. This value does not match the issue's own stream scope or any configured stream, so it is likely wrong. Do not assume the PSIRT value is correct. Step 3 will correct it based on lock-file evidence from Step 2, after engineer confirmation.

## Ecosystem Detection

| Item | Value |
|------|-------|
| Ecosystem | **Cargo** (Rust crate quinn-proto) |
| Listed in Ecosystem Mappings? | Yes, for both streams (`Cargo.lock`, `git show <tag>:Cargo.lock`) |
| Category | Source dependency: 2 remediation tasks per affected stream (upstream backport or dependency bump, plus downstream propagation) |

## Deployment Context

| Item | Value |
|------|-------|
| Affected repository | rhtpa-backend (the only Cargo source repository; the matrix `backend` column) |
| Deployment context | `upstream` (default, because the Source Repositories table has no Deployment Context column) |

## Next Steps

Step 1.5 (MITRE/OSV enrichment) comes next. Step 1.7 is skipped because no embargo policy URL is configured. Step 2 follows. External lookups were not performed, per the eval instructions.
