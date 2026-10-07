# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | (no comments) |

## Stream Scope Resolution

Issue summary suffix: `[rhtpa-2.2]` maps to stream **2.2.x**.

The issue is **scoped** to the 2.2.x stream. Steps 3 and 4 apply only to
versions within that stream. Cross-stream impact on other streams (2.1.x)
is handled via Case A (proactive remediation).

## Ecosystem Detection

Library: quinn-proto (Rust crate)
Ecosystem: **Cargo** (source dependency)
Classification: Source dependency -- 2 tasks per stream (upstream fix + downstream propagation)

Lock File: `Cargo.lock`
Check Command: `git show <tag>:Cargo.lock`

## Deployment Context Lookup

The Source Repositories table does not have a Deployment Context column.
Per backward compatibility rules, coordination guidance is omitted from
remediation task descriptions.

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Tag | quinn-proto | Affected? | Notes |
|--------|---------|-----|-------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | |

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Latest Tag Version | Fixed? |
|--------|-----------|-----------------|-------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (v0.4.12) | YES |

- **2.2.x**: fix already available on upstream branch release/0.4.z --
  remediation is a dependency bump (`cargo update`) plus downstream propagation.
- **2.1.x**: fix NOT available on upstream branch release/0.3.z --
  remediation requires upstream backport first, then downstream propagation.

## Affects Versions Correction

PSIRT-assigned Affects Versions: `[RHTPA 2.0.0]` -- **incorrect**.
Version RHTPA 2.0.0 does not exist in the configured streams.

Proposed correction (scoped to 2.2.x stream):
`Current: [RHTPA 2.0.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Versions 2.2.3 and 2.2.4 are excluded because they ship quinn-proto 0.11.14
(at or above the fix threshold).

## Cross-Stream Impact (Case A)

The 2.1.x stream is also affected (all versions ship quinn-proto 0.11.9),
but this issue is scoped to 2.2.x. Cross-stream impact is handled via
Case A proactive remediation -- preemptive tasks are created for 2.1.x
with the `security-preemptive` label.
