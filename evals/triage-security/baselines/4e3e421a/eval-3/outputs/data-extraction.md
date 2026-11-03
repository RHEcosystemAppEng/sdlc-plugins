# Step 1 – Data Extraction: TC-8003

Source: the mock Jira issue (`vuln-issue-duplicate.md`). No Jira MCP calls were made; the eval inputs stood in for the `jira.get_issue` and `jira.get_issue_remote_links` responses.

## Step 0 – Configuration (from claude-md-security-config.md)

| Setting | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source repositories | rhtpa-backend (deployment context: not specified, so it defaults to `upstream`) |

Matrix staleness (Step 0.3): the matrix has `Last-Updated: 2026-06-28T10:00:00Z`. The newest matrix row is 2.2.4 (2026-05-04). Today is 2026-11-03, so the matrix is roughly 4 months old. The engineer should check whether any 2.2.x release after 2.2.4 is missing from the matrix. This does not block triage.

## Extracted fields

| Field | Value |
|---|---|
| Issue key | TC-8003 |
| Issue status | New (so full triage runs) |
| CVE ID | CVE-2026-31812 (from the label and the summary) |
| Affected component | `pscomponent:org/rhtpa-server`, which maps to the rhtpa-backend Cargo workspace |
| PSIRT-claimed product version (summary suffix) | `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | quinn-proto (Rust crate) |
| Affected version range | < 0.11.14 ("versions before 0.11.14") |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High), DoS (panic on an excessive STREAMS frame count) |
| Upstream fix PR | None in the remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 (already past as of 2026-11-03) |
| Assignee | Unassigned |
| Existing comments | None |

## Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to stream **2.2.x**, which is configured (Konflux repo `rhtpa-release.0.4.z`).
- **Issue stream scope: 2.2.x.** The issue is scoped to that stream.

## Ecosystem detection

- quinn-proto is a Rust crate, so the ecosystem is **Cargo**. Cargo is listed in both streams' Ecosystem Mappings, with lock file `Cargo.lock` in the `backend` repo.
- Category: source dependency. A remediation would need 2 tasks per stream (upstream backport or dependency bump, plus downstream propagation).

## Step 1.5 / 1.7 notes

- External enrichment (MITRE and OSV) was not queried, because the eval does not allow external tools. The analysis uses the Jira description threshold (< 0.11.14, fixed in 0.11.14), so confidence in the threshold is lower.
- Embargo check: CVSS 7.5 meets the threshold of 7.0 or higher, but no Embargo policy URL is configured, so the step is skipped silently.

## Step 2 – Version Impact Analysis (simulated `git show <tag>:Cargo.lock`)

| Stream | Version | backend tag | quinn-proto | Affected (< 0.11.14)? | Notes |
|---|---|---|---|---|---|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.8 | — | YES | same as 2.2.1 (backend retag of 2.2.1) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | fixed |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | fixed |

- Development stream: no unreleased Jira version data was provided, and 2.2.x is the latest stream in the matrix. No development-head evidence is available.
- Upstream fix status: the fix (0.11.14) already ships from 2.2.3 onward on `release/0.4.z`. It is absent from all 2.1.x builds.
- **Affected versions scoped to this stream (2.2.x):** RHTPA 2.2.0, 2.2.1, 2.2.2.
- **Affected versions in other streams:** RHTPA 2.1.0 and 2.1.1 (stream 2.1.x).

## Step 3 – Affects Versions comparison (scoped to 2.2.x)

`Current: [RHTPA 2.2.0] → Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

The PSIRT value is correct but incomplete. Step 4 found that this issue is a same-stream duplicate, so the correction belongs on the surviving issue TC-7999 and is not applied to TC-8003 (see duplicate-check.md).
