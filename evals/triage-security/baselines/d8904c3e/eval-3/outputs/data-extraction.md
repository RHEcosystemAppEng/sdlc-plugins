# Step 1 -- Data Extraction: TC-8003

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x (mapped from summary suffix [rhtpa-2.2] to Version Streams table) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |
| Assignee | Unassigned |
| Status | New |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. This maps to the `2.2.x` stream in the Version Streams table of Security Configuration, which corresponds to the Konflux release repo `rhtpa-release.0.4.z`.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. Per the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, the ecosystem is **Cargo**. Cargo is classified as a **source dependency** ecosystem, which means remediation would produce 2 tasks per stream (upstream backport + downstream propagation).

The lock file for inspection is `Cargo.lock`, accessed via the check command `git show <tag>:Cargo.lock`.

## Version Impact Analysis (Step 2)

Using the security-matrix.md data for stream 2.2.x (rhtpa-release.0.4.z):

| Version | Build Tag | quinn-proto Version | Vulnerable? | Notes |
|---------|-----------|---------------------|-------------|-------|
| RHTPA 2.2.0 | v0.4.5 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| RHTPA 2.2.1 | v0.4.8 | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| RHTPA 2.2.2 | v0.4.9 | 0.11.12 | YES | Retag of v0.4.8 -- same as RHTPA 2.2.1 |
| RHTPA 2.2.3 | v0.4.11 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed version) |
| RHTPA 2.2.4 | v0.4.12 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed version) |

Affected versions in stream 2.2.x: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

The vulnerability was fixed starting in RHTPA 2.2.3 (build tag v0.4.11), which ships quinn-proto 0.11.14.

## Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Versions is incomplete:

- Current: [RHTPA 2.2.0]
- Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]

RHTPA 2.2.1 and RHTPA 2.2.2 are missing from the current Affects Versions. Both ship quinn-proto versions below the 0.11.14 fix threshold.

However, since this issue is identified as a duplicate in Step 4 (see duplicate-check.md), the Affects Versions correction would not be applied to TC-8003. The sibling issue TC-7999 should carry the correct Affects Versions instead.
