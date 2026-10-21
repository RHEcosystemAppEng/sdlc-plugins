# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 (PSIRT-assigned -- likely incorrect) |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry for 2.2.x)
- Issue is **scoped** to the 2.2.x stream

## Ecosystem Detection

- Ecosystem: **Cargo** (Rust crate: quinn-proto)
- Category: Source dependency
- Remediation pattern: 2 tasks per stream (dependency bump or upstream backport + downstream propagation)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`

## Deployment Context

- Repository: rhtpa-backend
- Deployment Context column: **absent** from Source Repositories table (backward compatibility)
- Default: `upstream` (applied implicitly; coordination guidance subsection omitted per template rules)

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | outside issue scope |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | outside issue scope |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | |

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Latest Tag Version | Fixed? |
|--------|-----------|-----------------|-------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (v0.4.12) | YES |

## Affects Versions Correction

- **Current** (PSIRT-assigned): RHTPA 2.0.0
- RHTPA 2.0.0 does not correspond to any supported version in the supportability matrix. This is incorrect.
- **Corrected** (within issue scope 2.2.x): RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- Versions RHTPA 2.2.3 and RHTPA 2.2.4 ship quinn-proto 0.11.14 and are NOT affected.

## Cross-Stream Impact (Case A)

Stream 2.1.x is also affected (versions 2.1.0, 2.1.1 both ship quinn-proto 0.11.9) but is outside this issue's scope. No sibling CVE Jira exists for `[rhtpa-2.1]`. Preemptive remediation tasks should be created for the 2.1.x stream.
