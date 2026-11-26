# Step 1 – Data Extraction (TC-8001)

Source: mock Jira issue `vuln-issue-standard.md` (simulated `jira.get_issue` and
`jira.get_issue_remote_links` output; no live Jira calls were made).

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8001 | Issue |
| Issue type / Status | Vulnerability / New | Issue |
| CVE ID | CVE-2026-31812 | Label `CVE-2026-31812` and summary text (consistent) |
| Affected component | `pscomponent:org/rhtpa-server` → `org/rhtpa-server` | Label matching pattern `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| Severity | CVSS 7.5 (High) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042: https://rustsec.org/advisories/RUSTSEC-2026-0042.html) | Remote links / description references |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Issue `duedate` |
| Assignee | Unassigned | Issue |
| Existing comments | None | Issue comment history |

All critical fields (CVE ID, library, affected range) were parsed successfully, so
execution does not need to stop for missing data.

## Stream Scope Resolution

| Item | Value |
|------|-------|
| Summary suffix | `[rhtpa-2.2]` |
| Mapped stream | **2.2.x** (git.example.com/rhtpa/rhtpa-release.0.4.z) |
| Scope | **Scoped** to a single stream (2.2.x); 2.1.x is outside this issue's scope |

## Ecosystem Detection

| Item | Value |
|------|-------|
| Ecosystem | Cargo (Rust crate) |
| Present in stream Ecosystem Mappings? | Yes (both 2.1.x and 2.2.x) |
| Category | Source dependency → 2 remediation tasks per affected stream |
| Lock file / check command | `Cargo.lock` / `git show <tag>:Cargo.lock` |

## Deployment Context

The affected component `org/rhtpa-server` does not match a row in the Source
Repositories table (only `rhtpa-backend`), and the table has no Deployment Context
column. Deployment context therefore defaults to **upstream**.

## Observations for Later Steps

- The PSIRT-assigned Affects Versions (**RHTPA 2.0.0**) does not match the summary
  suffix (`[rhtpa-2.2]`) and there is no configured 2.0.x stream. Step 3 will verify it
  against lock-file evidence and correct it.
- CVSS 7.5 meets the Step 1.7 threshold, but no Embargo policy URL is configured, so
  Step 1.7 is skipped.
