# Step 1 – Data Extraction (TC-8001)

Source: `vuln-issue-standard.md` (simulated `jira.get_issue` + `jira.get_issue_remote_links`; no Jira calls made).

## Extracted CVE data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8001 | Issue |
| Issue status | New (proceed with full triage) | Issue status |
| CVE ID | CVE-2026-31812 | Label `CVE-2026-31812` and summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching Component label pattern `pscomponent:` |
| Product version (PSIRT-claimed) | `rhtpa-2.2` | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| CVSS / severity | 7.5 (High) — DoS (panic on excessive stream count) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042: https://rustsec.org/advisories/RUSTSEC-2026-0042.html) | Remote links / description references |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Issue `duedate` |
| Assignee | Unassigned | Issue |
| Existing comments | None | Comment history |

All critical fields (CVE ID, library, affected range) parsed successfully — no engineer input required.

## Stream scope resolution

| Item | Value |
|------|-------|
| Summary suffix | `[rhtpa-2.2]` |
| Mapped stream | **2.2.x** (git.example.com/rhtpa/rhtpa-release.0.4.z) |
| Scope | **Scoped** to 2.2.x — Steps 2–8 treat 2.2.x as the issue's stream; other affected streams (e.g., 2.1.x) would be handled via Case A cross-stream logic |

## Ecosystem detection

| Item | Value |
|------|-------|
| Ecosystem | Cargo (Rust crate) |
| Listed in stream Ecosystem Mappings? | Yes (both 2.1.x and 2.2.x) |
| Lock file / check command | `Cargo.lock` via `git show <tag>:Cargo.lock` in `backend` |
| Category | Source dependency → 2 remediation tasks per affected stream |

## Deployment context

The Source Repositories table has no Deployment Context column, so all repos default
to `upstream`. Component `org/rhtpa-server` is not listed by that name (the closest
match is `rhtpa-backend`), so it also defaults to `upstream`.

## Observations to carry into later steps

- PSIRT Affects Versions (`RHTPA 2.0.0`) does not match the summary's stream (`rhtpa-2.2`). There is no 2.0.x stream configured, so this value looks wrong and will be checked against lock-file evidence in Step 3.
- CVSS 7.5 is at or above the embargo threshold. No Embargo policy URL is configured, though, so Step 1.7 is skipped.
