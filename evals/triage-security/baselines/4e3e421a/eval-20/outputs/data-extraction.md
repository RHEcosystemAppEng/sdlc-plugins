# Step 1 – Data Extraction (TC-8001)

Source: mock Jira issue `vuln-issue-standard.md`. No Jira MCP call was made; the fixture stands in for `jira.get_issue` and `jira.get_issue_remote_links`.

## Extracted CVE data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8001 | Issue |
| Status | New (full triage path) | Issue status |
| CVE ID | CVE-2026-31812 | Label `CVE-2026-31812` and summary text (the two agree) |
| Affected component | `pscomponent:org/rhtpa-server` (component: `org/rhtpa-server`) | Label matching the pattern `pscomponent:` |
| Product version (PSIRT-claimed) | `rhtpa-2.2` | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto (Rust crate) | Description |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| Severity | CVSS 7.5 (High), denial of service (panic on excessive stream count) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 (quinn-rs/quinn#2048) | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (GHSA-2026-qp73-x4mq); also RUSTSEC-2026-0042 (https://rustsec.org/advisories/RUSTSEC-2026-0042.html) | Remote links and description references |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Issue `duedate` |
| Assignee | Unassigned | Issue |
| Existing comments | None | Issue comment history |

All critical fields (CVE ID, library, affected range) were parsed, so nothing has to be requested from the engineer.

## Stream scope resolution

| Item | Value |
|------|-------|
| Summary suffix | `[rhtpa-2.2]` |
| Mapped Version Stream | **2.2.x** (git.example.com/rhtpa/rhtpa-release.0.4.z) |
| Scope | **Scoped** to the 2.2.x stream. Steps 3–4 apply to 2.2.x only. Other affected streams (such as 2.1.x) are handled through Case A (cross-stream impact). |

## Ecosystem detection

| Item | Value |
|------|-------|
| Ecosystem | Cargo (quinn-proto is a Rust crate) |
| Listed in stream Ecosystem Mappings | Yes (Cargo, backend repo, `Cargo.lock`, upstream branch `release/0.4.z` for 2.2.x and `release/0.3.z` for 2.1.x) |
| Category | Source dependency: 2 remediation tasks per affected stream (upstream backport or dependency bump, plus downstream propagation) |
| Lock file / check command | `Cargo.lock` / `git show <tag>:Cargo.lock` |

## Deployment context

| Item | Value |
|------|-------|
| Affected repository | rhtpa-backend (backend), from the Source Repositories table / matrix `backend` column |
| Deployment context | `upstream` (default: the Source Repositories table has no Deployment Context column) |

## Notes for later steps

- PSIRT's Affects Versions value (**RHTPA 2.0.0**) does not match the issue's own stream suffix (`rhtpa-2.2` → 2.2.x). There is no 2.0.x stream configured. Step 3 must check this against lock file evidence and is expected to correct it.
- An Embargo policy URL is not configured, so Step 1.7 will be skipped even though CVSS is 7.5 (at or above 7.0).
- VEX Justification field `customfield_12345` is configured for any Not a Bug closure.
