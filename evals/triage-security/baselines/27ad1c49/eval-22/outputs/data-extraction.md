# Data Extraction (Step 1) -- TC-8021

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |
| Upstream Affected Component (customfield_10632) | quinn-proto |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the configured Version Streams table. The issue is therefore **scoped** to the 2.2.x stream only. Steps 3 and 4 will operate within this scope, while Case A cross-stream analysis will check whether other streams (2.1.x) are also affected.

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, this maps to the **Cargo** ecosystem.

- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`
- Ecosystem category: **Source dependency** -- produces 2 remediation tasks per stream (upstream backport or dependency bump + downstream propagation)

## Deployment Context Lookup

The affected repository identified from the component label `pscomponent:org/rhtpa-server` is **rhtpa-backend**. The Source Repositories table does not include a Deployment Context column, so the default deployment context of `upstream` applies. However, because the Deployment Context column is absent from the table entirely, coordination guidance will be omitted from remediation task descriptions per backward compatibility rules.

## Version Impact Analysis (Step 2)

Using the mock lock file data from security-matrix-mock.md, the version impact for quinn-proto (fix threshold: >= 0.11.14) across all streams is:

### Full Version Impact Table

| Version | Stream | Tag | quinn-proto version | Affected? | Notes |
|---------|--------|-----|---------------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | < 0.11.14 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as 2.2.1, quinn-proto 0.11.12) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | >= 0.11.14, fixed |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | >= 0.11.14, fixed |

### Stream-Scoped Impact (2.2.x only, per issue scope)

Within the issue's scoped stream (2.2.x):
- **Affected**: 2.2.0, 2.2.1, 2.2.2
- **Not affected**: 2.2.3, 2.2.4

### Cross-Stream Impact (outside issue scope)

Stream 2.1.x is also affected (both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9), but this stream is outside the current issue's scope. This triggers Case A (cross-stream impact) in Step 8.

## Affects Versions Assessment (Step 3)

Current PSIRT-assigned Affects Versions: `RHTPA 2.0.0`

This is **incorrect**. There is no version 2.0.0 in the supportability matrix or the configured version streams. Based on lock file evidence for the scoped stream (2.2.x), the correct Affects Versions should be:

- RHTPA 2.2.0 (affected, quinn-proto 0.11.9)
- RHTPA 2.2.1 (affected, quinn-proto 0.11.12)
- RHTPA 2.2.2 (affected, retag of 2.2.1)

Versions 2.2.3 and 2.2.4 are NOT affected (ship quinn-proto 0.11.14, which is the fix version) and should NOT be in Affects Versions.

Proposed correction: `Current: [RHTPA 2.0.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
