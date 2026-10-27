# Step 1 -- Data Extraction

## Issue: TC-8001

### Parsed CVE Data Table

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description |
| Fixed version | 0.11.14 | Description |
| CVSS | 7.5 (High) | Description |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) | Remote links |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) | Remote links |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comment history |
| Issue status | New | Issue `status` field |
| Assignee | Unassigned | Issue `assignee` field |

### Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry for rhtpa-release.0.4.z)
- Issue is **stream-scoped** to 2.2.x

### Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Category: Source dependency
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z` (for 2.2.x stream)
- Remediation task count per stream: 2 (upstream backport or dependency bump + downstream propagation)

### Deployment Context

- Affected repository: rhtpa-backend
- Deployment context: **upstream** (from Source Repositories table; no Deployment Context column present, defaults to upstream)

### Affects Versions Mismatch (Preliminary)

The PSIRT-assigned Affects Versions is **RHTPA 2.0.0**, but the issue summary suffix `[rhtpa-2.2]` maps to the **2.2.x** stream. The 2.0.x stream is not configured in the Version Streams table. This mismatch will be corrected in Step 3 after the version impact analysis in Step 2 determines which versions actually ship the vulnerable dependency.

### Quinn-proto Version Impact (from mock lock file data)

For reference, the mock lock file data shows the following quinn-proto versions by build tag:

| Stream | Version | Build Tag | quinn-proto version | Vulnerable? (< 0.11.14) |
|--------|---------|-----------|---------------------|------------------------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES |
| 2.2.x | 2.2.2 | v0.4.9 | (retag of v0.4.8) 0.11.12 | YES (same as 2.2.1) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO (fixed) |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO (fixed) |

Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (the fixed version) and are not affected. All earlier versions across both streams ship vulnerable versions of quinn-proto (< 0.11.14).
