# Step 1 -- Data Extraction

## Issue: TC-8001

### Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description |
| Fixed version | 0.11.14 | Description |
| CVSS | 7.5 (High) | Description |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) | Remote links |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) | Remote links |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) | Remote links |
| Due date | 2026-07-15 | Jira `duedate` field |
| Existing comments | None | Jira comments |
| Assignee | Unassigned | Jira `assignee` field |
| Status | New | Jira `status` field |

### Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Parsed stream: **2.2.x**
- Matches configured Version Stream: **Yes** -- 2.2.x at `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Scope: **Scoped to 2.2.x stream only**

Steps 3-4 will apply only to the 2.2.x stream. Other streams (2.1.x) will be
checked for cross-stream impact in Step 2 but Affects Versions corrections in
Step 3 will be scoped to 2.2.x versions only.

### Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch (2.2.x stream): `release/0.4.z`
- Source repository: rhtpa-backend

Cargo is listed in both streams' Ecosystem Mappings tables, confirming
automated triage is supported.

### Deployment Context

- Repository: rhtpa-backend
- Deployment context: **upstream** (default -- no Deployment Context column in Source Repositories table)

### Affects Versions Discrepancy (Preliminary)

The Jira Affects Versions field currently lists **RHTPA 2.0.0**, but this issue
is scoped to the **2.2.x** stream (per the `[rhtpa-2.2]` suffix). There is no
2.0.x stream configured in the Version Streams table. This discrepancy will be
corrected in Step 3 after the version impact analysis in Step 2 determines
which 2.2.x versions actually ship the vulnerable dependency.

### Remediation Implications

As a Cargo (source dependency) ecosystem vulnerability, remediation will require
**two tasks** per affected stream:
1. Upstream backport task -- update quinn-proto to >= 0.11.14 in the source repo (rhtpa-backend)
2. Downstream propagation subtask -- update the pinned reference in the Konflux release repo (rhtpa-release.0.4.z)
