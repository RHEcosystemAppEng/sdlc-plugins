# Step 1 -- Data Extraction for TC-8020

## Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels (`CVE-2026-31812`) and summary text |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching component label pattern `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) | Remote links |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) | Remote links |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comment history |
| Upstream Affected Component | quinn-proto | customfield_10632 |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. This maps to the **2.2.x** version stream in the configured Version Streams table.

- Suffix parsed: `[rhtpa-2.2]` -> stream `2.2.x`
- Match found: 2.2.x stream (Konflux Release Repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`)
- **Issue stream scope**: 2.2.x

Because the issue is stream-scoped, Steps 3 and 4 will apply only to versions in the 2.2.x stream. Cross-stream impact for 2.1.x (if any) will be handled via Case A (cross-stream impact comment and preemptive remediation tasks).

## Ecosystem Detection

- Vulnerable library: quinn-proto (Rust crate)
- Detected ecosystem: **Cargo**
- Category: Source dependency
- Remediation tasks per stream: 2 (upstream backport or dependency bump + downstream propagation)

The Cargo ecosystem is listed in both the 2.1.x and 2.2.x stream Ecosystem Mappings tables. The lock file is `Cargo.lock` with check command `git show <tag>:Cargo.lock`.

## Deployment Context Lookup

- Affected repository: rhtpa-backend (from component label `pscomponent:org/rhtpa-server` mapped to Source Repositories)
- Deployment context: **upstream** (from Source Repositories table; the Deployment Context column is absent, so defaults to `upstream`)

## Version Impact Analysis (Step 2)

Using the mock lock file data from security-matrix-mock.md:

### Version Impact Table

| Version | Stream | quinn-proto version | Affected? | Notes |
|---------|--------|---------------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | 2.1.x | 0.11.9 | YES | < 0.11.14 |
| 2.2.0 | 2.2.x | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 2.2.x | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as 2.2.1: 0.11.12) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | = fix version (0.11.14) |
| 2.2.4 | 2.2.x | 0.11.14 | NO | = fix version (0.11.14) |

### Stream-scoped impact summary (2.2.x only, per issue scope)

- Affected: 2.2.0, 2.2.1, 2.2.2
- Not affected: 2.2.3, 2.2.4

### Cross-stream impact (outside issue scope)

- 2.1.x stream: 2.1.0 and 2.1.1 are ALSO affected (quinn-proto 0.11.9 < 0.11.14)

## Affects Versions Assessment

- **Current Affects Versions**: RHTPA 2.0.0
- **Problem**: RHTPA 2.0.0 does not correspond to any configured version stream (no 2.0.x stream exists). This is a PSIRT assignment error.
- **Proposed correction** (scoped to 2.2.x stream): RHTPA 2.2.0, RHTPA 2.2.1
  - Version 2.2.2 is a retag of 2.2.1 and may or may not have a separate Jira version entry.
  - Versions 2.2.3 and 2.2.4 are NOT affected (ship quinn-proto 0.11.14).
  - Versions 2.1.0 and 2.1.1 belong to the 2.1.x stream and are out of scope for this issue's Affects Versions.
