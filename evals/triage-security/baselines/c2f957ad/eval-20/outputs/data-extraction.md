# Step 1 – Data Extraction — TC-8001

Source: mock Jira issue `vuln-issue-standard.md` (simulated `jira.get_issue` and
`jira.get_issue_remote_links` output; no external calls made).

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8001 | Issue key |
| Issue type / Status | Vulnerability / New | Issue fields (status-aware handling: New → full triage) |
| CVE ID | CVE-2026-31812 | Label `CVE-2026-31812` and summary text (consistent) |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching Component label pattern `pscomponent:` |
| Product version (PSIRT-claimed) | rhtpa-2.2 → stream **2.2.x** | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| Severity | CVSS 7.5 (High) — Denial of Service (panic on excessive stream count) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 (quinn-rs/quinn#2048) | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042: https://rustsec.org/advisories/RUSTSEC-2026-0042.html) | Remote links / description references |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Assignee | Unassigned | Issue field |
| Existing comments | None | Issue comment history |

All critical fields (CVE ID, vulnerable library, affected range) were parsed
successfully — no engineer input required to continue.

## Stream Scope Resolution

| Item | Value |
|------|-------|
| Summary suffix | `[rhtpa-2.2]` |
| Parsed stream | 2.2.x |
| Matching configured Version Stream | 2.2.x — git.example.com/rhtpa/rhtpa-release.0.4.z |
| Issue stream scope | **Scoped to 2.2.x** (Steps 2–8 analyze only this stream) |

## Ecosystem Detection

| Item | Value |
|------|-------|
| Ecosystem | **Cargo** (quinn-proto is a Rust crate) |
| Supported in stream Ecosystem Mappings? | Yes — 2.2.x: Cargo / backend / `Cargo.lock` / `git show <tag>:Cargo.lock` / upstream branch `release/0.4.z` |
| Category | Source dependency — 2 remediation tasks per affected stream (upstream backport/bump + downstream propagation) |

## Deployment Context

| Item | Value |
|------|-------|
| Affected repository | rhtpa-backend (matrix column `backend`) |
| Deployment context | `upstream` (Source Repositories table has no Deployment Context column → backward-compatible default) |

## Observations for Later Steps

- **Affects Versions mismatch:** The Jira field lists `RHTPA 2.0.0`, which does not
  belong to the PSIRT-claimed 2.2.x stream (and no 2.0.x stream is configured). This
  will be validated against lock-file evidence and corrected in Step 3.
- Preview of matrix lock data for the scoped 2.2.x stream (to be confirmed in Step 2):
  quinn-proto 0.11.9 at `v0.4.5` (2.2.0) and 0.11.12 at `v0.4.8` (2.2.1, and 2.2.2 as a
  backend retag) are below 0.11.14 (vulnerable); `v0.4.11` (2.2.3) and `v0.4.12` (2.2.4)
  ship 0.11.14 (fixed).
