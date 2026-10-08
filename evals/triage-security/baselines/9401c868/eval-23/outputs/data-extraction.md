# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | (no comments) | Issue comment history |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream
(Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

This issue is **scoped** to the 2.2.x stream. Steps 3 and 4 apply only to 2.2.x versions;
cross-stream impact on other streams (e.g., 2.1.x) is handled by Case A in Step 8.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. Based on the Ecosystem Mappings tables
in both streams' security-matrix.md files, the ecosystem is **Cargo**.

- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
- Ecosystem category: Source dependency
- Remediation tasks per stream: 2 (dependency bump + downstream propagation, since the fix is available upstream for 2.2.x)

## Deployment Context Lookup

The affected component label `pscomponent:org/rhtpa-server` maps to the source repository
**rhtpa-backend** in the Source Repositories table.

| Repository | URL | Local Path | Deployment Context |
|------------|-----|------------|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | **customer-shipped** |

Deployment context for rhtpa-backend: **customer-shipped**

This deployment context will be used in Step 8 (Remediation) to generate coordination guidance
in remediation task descriptions. The `customer-shipped` context requires coordination with
Product Security for CVE assignment, advisory preparation, and formal disclosure.

## Version Impact Analysis

Using the supportability matrices and mock lock file data for quinn-proto:

### Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto versions before 0.11.14):

| Stream | Version | Build Tag | quinn-proto | Affected? | Notes |
|--------|---------|-----------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | fixed version |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | fixed version |

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix Available? | Notes |
|--------|-----------|-----------------|----------------|-------|
| 2.2.x | Cargo | release/0.4.z | YES | v0.4.11 already ships quinn-proto 0.11.14 |
| 2.1.x | Cargo | release/0.3.z | NO | Latest tag v0.3.12 ships quinn-proto 0.11.9 |

### Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Versions is `RHTPA 2.0.0`, which does not correspond to any
version in the supportability matrix. The issue is scoped to stream 2.2.x.

Affected 2.2.x versions based on lock file evidence: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

Proposed correction:
- Current: `[RHTPA 2.0.0]`
- Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

(Versions 2.2.3 and 2.2.4 are NOT affected -- they ship quinn-proto 0.11.14 which is the fixed version.)

### Cross-Stream Impact Summary

The issue is scoped to **2.2.x**, but stream **2.1.x** is also affected:
- 2.1.0 ships quinn-proto 0.11.9 (affected)
- 2.1.1 ships quinn-proto 0.11.9 (affected)

This triggers **Case A** (cross-stream impact) in Step 8, which creates preemptive
remediation tasks for the 2.1.x stream if no sibling CVE Jira exists for that stream.
