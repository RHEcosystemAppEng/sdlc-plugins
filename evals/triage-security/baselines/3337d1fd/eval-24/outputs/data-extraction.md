# Step 1 -- Data Extraction: TC-8001

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

Issue summary suffix `[rhtpa-2.2]` maps to configured Version Stream **2.2.x** (Konflux release repo: rhtpa-release.0.4.z). This issue is **scoped** to the 2.2.x stream.

## Ecosystem Detection

Library: quinn-proto (Rust crate). Ecosystem: **Cargo**. Configured in both streams' Ecosystem Mappings tables with lock file `Cargo.lock`.

## Deployment Context

The Source Repositories table does not include a Deployment Context column. Per backward-compatibility rules, deployment context defaults to `upstream` for internal tracking. Coordination Guidance is omitted from remediation task descriptions.

## Version Impact Table

Version impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | |
| 2.2.4 | 2.2.x | 0.11.14 | NO | |

## Affects Versions Correction

- **Current** (PSIRT-assigned): RHTPA 2.0.0
- **Proposed** (scoped to 2.2.x stream, based on lock file evidence): RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Rationale**: PSIRT assigned RHTPA 2.0.0 which does not exist as a configured stream. Lock file analysis at pinned commits shows quinn-proto < 0.11.14 in versions 2.2.0, 2.2.1, and 2.2.2 within the 2.2.x stream.

## Cross-Stream Impact (Case B)

Stream 2.1.x is also affected (versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9). Since this issue is scoped to 2.2.x, the 2.1.x impact is reported as cross-stream and requires preemptive remediation tasks (assuming no existing sibling CVE Jira for the 2.1.x stream).

## Triage Outcome

- **Case A**: Create remediation tasks for 2.2.x stream (versions 2.2.0, 2.2.1, 2.2.2 affected)
- **Case B**: Create preemptive remediation tasks for 2.1.x stream (versions 2.1.0, 2.1.1 affected; no sibling CVE Jira)
- Ecosystem is Cargo (source dependency) so each stream gets two tasks: upstream backport + downstream propagation
