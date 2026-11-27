# Step 1 – Data Extraction (TC-8001)

Source: mock Jira issue `vuln-issue-standard.md` (Jira and remote-link fetches simulated; no external calls made).

## Extracted CVE data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8001 | Issue |
| Issue type / Status | Vulnerability / New | Issue |
| CVE ID | CVE-2026-31812 | Label `CVE-2026-31812` + summary (match) |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching pattern `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` → RHTPA 2.2 | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | `versions` field |
| Vulnerable library | quinn-proto | Description |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| Severity / CVSS | 7.5 (High), denial of service (panic on excessive stream count) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042: https://rustsec.org/advisories/RUSTSEC-2026-0042.html) | Remote links / description references |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | `duedate` field |
| Assignee | Unassigned | Issue |
| Existing comments | None | Comment history |

All critical fields (CVE ID, library, affected range) were parsed, so there is no need to ask the engineer for missing data.

## Stream scope resolution

| Item | Value |
|------|-------|
| Summary suffix | `[rhtpa-2.2]` |
| Mapped stream | **2.2.x** (git.example.com/rhtpa/rhtpa-release.0.4.z, local path /home/dev/repos/rhtpa-release.0.4.z) |
| Issue scope | **Scoped**: Steps 2–8 analyze only the 2.2.x stream |

## Ecosystem detection

| Item | Value |
|------|-------|
| Ecosystem | **Cargo** (Rust crate quinn-proto) |
| Listed in 2.2.x Ecosystem Mappings | Yes: repository `backend`, lock file `Cargo.lock`, check command `git show <tag>:Cargo.lock`, upstream branch `release/0.4.z` |
| Category | Source dependency: 2 remediation tasks per affected stream (upstream backport + downstream propagation) |

## Deployment context

The component label `org/rhtpa-server` does not directly name a configured Source Repository. The only configured source repo is `rhtpa-backend` (https://github.com/rhtpa/rhtpa-backend), which is the Cargo `backend` repository in the matrix. The Source Repositories table has no Deployment Context column, so the deployment context defaults to **`upstream`**.

## Observations to carry forward

- **Affects Versions mismatch**: the Jira field says `RHTPA 2.0.0`, but the summary scopes the issue to RHTPA 2.2 (stream 2.2.x), and no 2.0.x stream is configured. Step 3 will correct this after the Step 2 version impact analysis.
- **Preview of matrix data** (from mock lock-file data for 2.2.x; Step 2 makes the final call): v0.4.5 (2.2.0) has quinn-proto 0.11.9 and v0.4.8 (2.2.1, 2.2.2 retag) has 0.11.12, both below 0.11.14. v0.4.11 (2.2.3) and v0.4.12 (2.2.4) have 0.11.14, which is the fixed version.
- Due date 2026-07-15 is 3 days after the evaluation clock (2026-07-12).
