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
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`). This issue is **scoped** to stream 2.2.x.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. Ecosystem: **Cargo** (source dependency). Lock file: `Cargo.lock`. Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`.

Per the ecosystem classification table, source dependency ecosystems produce **2 remediation tasks per stream** (upstream backport + downstream propagation).

## Deployment Context Lookup

The affected component label `pscomponent:org/rhtpa-server` maps to source repository **rhtpa-backend** in the Source Repositories table from Security Configuration.

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | **customer-shipped** |

Deployment context for rhtpa-backend: **customer-shipped**

This deployment context will be used in Step 8 (Remediation) to generate coordination guidance in remediation task descriptions.

## Version Impact Analysis

### quinn-proto versions by pinned commit

**Stream 2.1.x (rhtpa-release.0.3.z):**

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.1.0 | `v0.3.8` | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | `v0.3.12` | 0.11.9 | YES | < 0.11.14 |

**Stream 2.2.x (rhtpa-release.0.4.z):**

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.2.0 | `v0.4.5` | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | `v0.4.8` | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | `v0.4.9` | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | `v0.4.11` | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | `v0.4.12` | 0.11.14 | NO | >= 0.11.14 (fixed) |

### Aggregated Version Impact Table

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | fixed |
| 2.2.4 | 2.2.x | 0.11.14 | NO | fixed |

### Affects Versions Correction

The PSIRT-assigned Affects Versions is `RHTPA 2.0.0`, which is incorrect -- there is no 2.0.x stream configured.

Since this issue is scoped to stream 2.2.x, the corrected Affects Versions (scoped to 2.2.x only) should be:

- Current: `[RHTPA 2.0.0]`
- Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Versions 2.2.3 and 2.2.4 are NOT affected (quinn-proto already at 0.11.14).

### Cross-Stream Impact

Stream 2.1.x is also affected (versions 2.1.0 and 2.1.1 ship quinn-proto 0.11.9). Since this issue is scoped to 2.2.x, the 2.1.x impact triggers Case A (cross-stream impact -- proactive remediation).

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Notes |
|--------|-----------|-----------------|-------|
| 2.2.x | Cargo | release/0.4.z | v0.4.11 already includes fix (0.11.14) -- upstream branch HEAD likely fixed |
| 2.1.x | Cargo | release/0.3.z | Latest tag v0.3.12 still at 0.11.9 -- upstream fix needed on this branch |
