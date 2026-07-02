# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope

Issue summary suffix `[rhtpa-2.2]` maps to stream **2.2.x** (Konflux release repo: rhtpa-release.0.4.z).

This issue is **stream-scoped** to 2.2.x. Steps 3 and 4 apply only to versions within that stream.

## Ecosystem

**Cargo** (Rust crate quinn-proto).

- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
- Source repository: backend (from Ecosystem Mappings)

## Deployment Context

**upstream** (default -- Deployment Context column is absent from the Source Repositories table in CLAUDE.md; all repositories default to `upstream` per backward-compatibility rule).

## Version Impact Table

Version impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | backend Tag | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | |

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | YES |

## Affects Versions Correction

Scoped to stream 2.2.x per issue suffix `[rhtpa-2.2]`.

- **Current**: RHTPA 2.0.0 (incorrect -- no version 2.0.0 exists in the supportability matrix)
- **Proposed**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14, which meets the fix threshold. They are NOT affected and are excluded from Affects Versions.

## Cross-Stream Impact

Stream 2.1.x is also affected (all versions ship quinn-proto 0.11.9, which is within the vulnerable range). This triggers Case B (cross-stream impact) in Step 8. The upstream branch `release/0.3.z` does NOT have the fix -- remediation is needed for this stream.
