# Step 1 -- Data Extraction

## Parsed CVE Data Table

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels: `CVE-2026-31812`; Summary text |
| Affected component | org/rhtpa-server | Label: `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix: `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description: "A vulnerability was found in quinn-proto" |
| Affected version range | < 0.11.14 | Description: "versions before 0.11.14" |
| Fixed version | 0.11.14 | Description: "Fixed version: 0.11.14" |
| CVSS | 7.5 (High) | Description: "CVSS: 7.5 (High)" |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote link: quinn-rs/quinn#2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote link: GitHub Advisory |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote link: CVE Record |
| Due date | 2026-07-15 | Jira `duedate` field |
| Existing comments | None | Issue comment history |
| Issue status | New | Jira `status` field |
| Assignee | Unassigned | Jira `assignee` field |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. Mapping this to the configured Version Streams:

- Suffix `rhtpa-2.2` maps to stream **2.2.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`)

The issue is **stream-scoped** to the 2.2.x stream.

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. This maps to the **Cargo** ecosystem as configured in the stream's Ecosystem Mappings table.

- Ecosystem: **Cargo**
- Category: **Source dependency**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z` (for 2.2.x stream)

Per the ecosystem classification table, a source dependency ecosystem produces **2 remediation tasks per affected stream**: upstream backport + downstream propagation (or dependency bump + downstream propagation if the upstream fix is already available).

## Deployment Context

The affected repository `rhtpa-backend` is listed in Source Repositories. No explicit Deployment Context column is present in the Source Repositories table, so the default deployment context of **upstream** applies.

## Affects Versions Observation

The PSIRT-assigned Affects Version is **RHTPA 2.0.0**, which does not correspond to any version in the supportability matrix (the matrix covers versions 2.1.0, 2.1.1, 2.2.0 through 2.2.4). This will require correction in Step 3 after version impact analysis confirms which versions are actually affected.
