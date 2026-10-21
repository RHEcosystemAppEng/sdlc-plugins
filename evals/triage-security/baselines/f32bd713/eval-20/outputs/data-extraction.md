# Step 1 -- Data Extraction

## Issue: TC-8001

### Parsed CVE Data Table

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description |
| Fixed version | 0.11.14 | Description |
| CVSS score | 7.5 (High) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 (quinn-rs/quinn#2048) | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Jira `duedate` field |
| Existing comments | None | Issue comment history |
| Issue status | New | Jira `status` field |
| Assignee | Unassigned | Jira `assignee` field |

### Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`.

- Parsed suffix: `rhtpa-2.2`
- Mapped stream: **2.2.x**
- Match in Version Streams table: **Yes** (2.2.x at git.example.com/rhtpa/rhtpa-release.0.4.z)
- Issue stream scope: **2.2.x** (scoped -- analysis targets only this stream for Steps 3-4, but all streams are checked for version impact in Step 2)

### Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Detected ecosystem: **Cargo**
- Category: Source dependency
- Remediation tasks per stream: 2 (upstream backport or dependency bump + downstream propagation)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`

### Deployment Context Lookup

- Affected repository (from component label `pscomponent:org/rhtpa-server`): rhtpa-backend
- Source Repositories match: rhtpa-backend (URL: https://github.com/rhtpa/rhtpa-backend)
- Deployment context: **upstream** (default -- no Deployment Context column in Source Repositories table)

### Affects Versions Discrepancy (preliminary)

The PSIRT-assigned Affects Versions field lists **RHTPA 2.0.0**, but the issue
summary suffix `[rhtpa-2.2]` and the Version Streams table show no 2.0.x stream.
The configured streams are 2.1.x and 2.2.x. This discrepancy will be corrected
in Step 3 after version impact analysis confirms which versions actually ship the
vulnerable dependency.
