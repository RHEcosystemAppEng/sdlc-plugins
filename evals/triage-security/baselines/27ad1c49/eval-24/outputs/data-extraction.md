# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 (versions before 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | (none) |

## Stream Scope

Issue summary suffix: `[rhtpa-2.2]`
Mapped stream: **2.2.x**
Issue is **scoped** to the 2.2.x stream.

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Category: Source dependency
- Remediation tasks per stream: 2 (upstream fix + downstream propagation)

## Deployment Context

- Repository: rhtpa-backend
- Deployment Context column: absent from Source Repositories table
- Coordination guidance: omitted (no Deployment Context column)

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0   | 2.1.x  | 0.11.9      | YES       |       |
| 2.1.1   | 2.1.x  | 0.11.9      | YES       |       |
| 2.2.0   | 2.2.x  | 0.11.9      | YES       |       |
| 2.2.1   | 2.2.x  | 0.11.12     | YES       |       |
| 2.2.2   | 2.2.x  | --          | YES       | retag of 2.2.1 |
| 2.2.3   | 2.2.x  | 0.11.14     | NO        |       |
| 2.2.4   | 2.2.x  | 0.11.14     | NO        |       |

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at Latest Tag | Fixed? |
|--------|-----------|-----------------|----------------------|--------|
| 2.2.x  | Cargo     | release/0.4.z   | 0.11.14 (at v0.4.11+) | YES   |
| 2.1.x  | Cargo     | release/0.3.z   | 0.11.9 (at v0.3.12)   | NO    |

## Affects Versions Correction (Step 3)

- Current (PSIRT-assigned): `[RHTPA 2.0.0]`
- RHTPA 2.0.0 does not exist as a valid version -- PSIRT version is wrong.
- Proposed (scoped to 2.2.x stream): `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
- Versions 2.2.3 and 2.2.4 are NOT affected (ship quinn-proto 0.11.14).
- Versions 2.1.0 and 2.1.1 are affected but belong to the 2.1.x stream (handled by sibling issues or preemptive tasks).

## Cross-Stream Impact (Case A)

This issue is scoped to stream 2.2.x, but version impact analysis reveals that stream 2.1.x is also affected:

| Stream | Affected Versions | Status |
|--------|-------------------|--------|
| 2.1.x  | 2.1.0, 2.1.1     | No sibling CVE Jira found -- preemptive remediation tasks needed |

## Triage Outcome

- **Case A**: Cross-stream impact -- 2.1.x is also affected. Create preemptive remediation tasks for 2.1.x (upstream backport variant, since fix is NOT available on release/0.3.z).
- **Case B**: Affected versions exist in the scoped 2.2.x stream. Create remediation tasks (dependency bump variant, since fix IS already available on release/0.4.z).
