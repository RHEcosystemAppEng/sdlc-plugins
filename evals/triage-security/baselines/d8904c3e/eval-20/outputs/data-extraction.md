# Step 1 -- Data Extraction

## Issue: TC-8001

Parsed from the Vulnerability issue fields, description, labels, and remote links.

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels (`CVE-2026-31812`) and summary text |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | < 0.11.14 (versions before 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links (quinn-rs/quinn#2048) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links (GitHub Advisory) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links (CVE Record) |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comment history |
| Issue status | New | Issue `status` field |
| Assignee | Unassigned | Issue `assignee` field |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`.

1. Parsed suffix: `rhtpa-2.2` maps to stream **2.2.x**
2. Match found: stream 2.2.x is configured in the Version Streams table
   (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`)
3. Issue stream scope: **2.2.x** (scoped to a single stream)

Because this is a scoped issue, Steps 3 and 4 will apply only to the 2.2.x
stream. However, Case A (cross-stream impact) will check whether other streams
(2.1.x) are also affected by the vulnerability.

## Ecosystem Detection

- Library: **quinn-proto** (a Rust crate)
- Detected ecosystem: **Cargo**
- Category: **Source dependency**
- Remediation tasks per stream: **2** (upstream backport + downstream propagation)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch (2.1.x): `release/0.3.z`
- Upstream branch (2.2.x): `release/0.4.z`

## Deployment Context Lookup

- Affected component from label: `pscomponent:org/rhtpa-server`
- Mapped repository: **rhtpa-backend** (from Source Repositories table)
- Repository URL: https://github.com/rhtpa/rhtpa-backend
- Deployment Context column: not present in Source Repositories table
- Deployment context: **upstream** (default, since no Deployment Context column exists)

## Affects Versions Mismatch Flag

The PSIRT-assigned Affects Versions field lists **RHTPA 2.0.0**, but:
- There is no 2.0.x stream configured in the Version Streams table
- The issue is scoped to stream 2.2.x (per the summary suffix `[rhtpa-2.2]`)
- The Affects Versions will need correction in Step 3 after the version impact
  analysis determines which 2.2.x versions actually ship the vulnerable dependency

## Verification Notes

All critical fields were successfully parsed:
- CVE ID: CVE-2026-31812 (present)
- Vulnerable library: quinn-proto (present)
- Affected version range: < 0.11.14 (present)
- Fixed version: 0.11.14 (present)

No missing critical fields -- proceed to Step 1.5 (External CVE Data Enrichment).
