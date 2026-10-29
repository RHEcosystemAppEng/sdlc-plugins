# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data

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
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Issue status | New |
| Assignee | Unassigned |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the configured **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`). This is a **stream-scoped** issue -- Steps 3-8 apply to the 2.2.x stream, with cross-stream impact analysis for other affected streams.

## Ecosystem Detection

The vulnerable library **quinn-proto** is a Rust crate. The Ecosystem Mappings tables for both streams list **Cargo** as the ecosystem with:
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branches: `release/0.3.z` (2.1.x stream), `release/0.4.z` (2.2.x stream)

Cargo is a **source dependency** ecosystem. Per the ecosystem classification table, this produces **2 tasks per affected stream**: upstream backport (or dependency bump) + downstream propagation.

## Deployment Context Lookup

The Source Repositories table in Security Configuration does NOT have a Deployment Context column. Per backward compatibility rules, coordination guidance is omitted entirely from remediation task descriptions.

## Step 2 -- Version Impact Analysis

### Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Build | Backend Tag | quinn-proto | Affected? | Notes |
|--------|---------|-------|-------------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | 0.3.8 | v0.3.8 | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | 0.3.12 | v0.3.12 | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | 0.4.5 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | 0.4.8 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | 0.4.9 | v0.4.8 | 0.11.12 | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.x | 2.2.3 | 0.4.11 | v0.4.11 | 0.11.14 | NO | >= fixed version |
| 2.2.x | 2.2.4 | 0.4.12 | v0.4.12 | 0.11.14 | NO | >= fixed version |

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Latest Tag Evidence | quinn-proto at Latest | Fixed? |
|--------|-----------|-----------------|---------------------|----------------------|--------|
| 2.1.x | Cargo | release/0.3.z | v0.3.12 | 0.11.9 | NO |
| 2.2.x | Cargo | release/0.4.z | v0.4.12 | 0.11.14 | YES |

**2.2.x stream**: The fix is already present on the upstream branch (`release/0.4.z`). Builds 0.4.11+ (product versions 2.2.3+) already ship quinn-proto 0.11.14. No new upstream or downstream remediation is required for this stream -- the vulnerability was resolved by a prior dependency update.

**2.1.x stream**: The upstream branch (`release/0.3.z`) does NOT have the fix. The latest release (v0.3.12) still ships quinn-proto 0.11.9. Remediation requires an upstream backport followed by downstream propagation.

## Step 3 -- Affects Versions Correction (PROPOSAL)

The PSIRT-assigned Affects Versions is **RHTPA 2.0.0**. There is no configured 2.0.x version stream, so this value is incorrect.

Based on lock file evidence, the correct Affects Versions for the scoped 2.2.x stream are:

- **RHTPA 2.2.0** -- quinn-proto 0.11.9 (affected)
- **RHTPA 2.2.1** -- quinn-proto 0.11.12 (affected)
- **RHTPA 2.2.2** -- quinn-proto 0.11.12 (affected, retag of 2.2.1)

Versions RHTPA 2.2.3 and RHTPA 2.2.4 are NOT affected (ship quinn-proto 0.11.14).

**PROPOSED Jira mutation**: Remove RHTPA 2.0.0, add RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2.

## Cross-Stream Impact Assessment (Case A)

The issue is scoped to the **2.2.x** stream. Version impact analysis reveals that the **2.1.x** stream is also affected:

- 2.1.0: quinn-proto 0.11.9 (affected)
- 2.1.1: quinn-proto 0.11.9 (affected)

No sibling CVE Jira exists for the 2.1.x stream (no `[rhtpa-2.1]` suffixed Vulnerability issue found). Preemptive remediation tasks are required for the 2.1.x stream.

**PROPOSED Jira comment** on TC-8001:
> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.

## Triage Outcome Summary

- **2.2.x stream (scoped)**: Fix already shipped in versions 2.2.3+. Affects Versions correction needed. No new remediation tasks required.
- **2.1.x stream (cross-stream)**: All versions affected. Upstream fix not available on release/0.3.z. Preemptive remediation tasks required (upstream backport + downstream propagation).
