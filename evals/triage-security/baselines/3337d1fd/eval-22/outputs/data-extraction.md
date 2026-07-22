# Step 1 -- Data Extraction for TC-8021

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches `pscomponent:` pattern) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Jira `duedate` field |
| Existing comments | None | Issue comment history |
| Upstream Affected Component | quinn-proto | customfield_10632 |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. Mapping:

- Parsed suffix: `rhtpa-2.2` --> stream `2.2.x`
- Matched to Version Streams table: **2.2.x** (Konflux release repo `rhtpa-release.0.4.z`)
- Issue stream scope: **2.2.x** (scoped issue -- Steps 3-4 apply only to this stream)

## Ecosystem Detection

The vulnerable library is `quinn-proto`, a Rust crate. This maps to the **Cargo** ecosystem, which is listed in the Ecosystem Mappings table for both the 2.1.x and 2.2.x streams.

- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branches: `release/0.3.z` (2.1.x), `release/0.4.z` (2.2.x)

## Deployment Context Lookup

The affected repository from the component label `pscomponent:org/rhtpa-server` maps to `rhtpa-backend` in the Source Repositories table. The Source Repositories table does not include a Deployment Context column, so the default of `upstream` applies.

## Version Impact Table

Using the mock lock file data from the security matrix:

| Version | Stream | backend Tag | quinn-proto Version | Affected? | Notes |
|---------|--------|-------------|---------------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | < 0.11.14 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Affects Versions Assessment

The PSIRT-assigned Affects Versions (`RHTPA 2.0.0`) is **incorrect**. There is no 2.0.x stream configured. The correct Affects Versions for the scoped stream (2.2.x) are:

- **RHTPA 2.2.0** -- ships quinn-proto 0.11.9 (affected)
- **RHTPA 2.2.1** -- ships quinn-proto 0.11.12 (affected)
- **RHTPA 2.2.2** -- retag of 2.2.1 (affected)

Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (the fixed version) and are NOT affected.

The 2.1.x stream (versions 2.1.0, 2.1.1) is also affected but belongs to a different stream scope and would be handled via cross-stream impact (Case B).
