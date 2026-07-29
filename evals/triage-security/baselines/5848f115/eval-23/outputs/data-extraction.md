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
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`).

- **Issue stream scope**: 2.2.x
- Steps 3 and 8 are scoped to the 2.2.x stream only.
- All streams (2.1.x and 2.2.x) are still analyzed in Step 2 for cross-stream impact detection.

## Ecosystem Detection

- **Library**: quinn-proto (Rust crate)
- **Ecosystem**: Cargo
- **Category**: Source dependency
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
- **Remediation tasks per stream**: 2 (upstream backport + downstream propagation)

## Deployment Context Lookup

The affected component label `pscomponent:org/rhtpa-server` maps to the source repository **rhtpa-backend**.

Lookup in Source Repositories table:

| Repository | URL | Local Path | Deployment Context |
|------------|-----|------------|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | **customer-shipped** |

**Deployment context**: `customer-shipped`

This deployment context will be used in Step 8 (Remediation) to generate coordination guidance in remediation task descriptions. Per the remediation templates, `customer-shipped` requires coordination with Product Security for CVE assignment, advisory preparation, and formal disclosure.

## Version Impact Analysis (Step 2)

### Supportability Matrix (Aggregated)

**Stream 2.1.x** (rhtpa-release.0.3.z):

| Version | Build | Build Date | Backend Tag | Source Pinning |
|---------|-------|------------|-------------|----------------|
| 2.1.0 | 0.3.8 | 2025-09-15 | v0.3.8 | artifacts.lock.yaml |
| 2.1.1 | 0.3.12 | 2025-11-20 | v0.3.12 | artifacts.lock.yaml |

**Stream 2.2.x** (rhtpa-release.0.4.z):

| Version | Build | Build Date | Backend Tag | Source Pinning | Notes |
|---------|-------|------------|-------------|----------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 | artifacts.lock.yaml | |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 | artifacts.lock.yaml | |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 | artifacts.lock.yaml | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 | artifacts.lock.yaml | |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 | artifacts.lock.yaml | |

### Dependency Version Extraction (Step 2.3)

quinn-proto versions extracted from `Cargo.lock` at each pinned backend tag:

| Tag | quinn-proto version | Source |
|-----|---------------------|--------|
| v0.3.8 | 0.11.9 | `git show v0.3.8:Cargo.lock` |
| v0.3.12 | 0.11.9 | `git show v0.3.12:Cargo.lock` |
| v0.4.5 | 0.11.9 | `git show v0.4.5:Cargo.lock` |
| v0.4.8 | 0.11.12 | `git show v0.4.8:Cargo.lock` |
| v0.4.9 | _(retag of v0.4.8)_ | same as v0.4.8 |
| v0.4.11 | 0.11.14 | `git show v0.4.11:Cargo.lock` |
| v0.4.12 | 0.11.14 | `git show v0.4.12:Cargo.lock` |

### Version Impact Table (Step 2.4)

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | at fix threshold |
| 2.2.4 | 2.2.x | 0.11.14 | NO | at fix threshold |

### Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Latest Tag Version | Fixed? |
|--------|-----------|-----------------|-------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (v0.4.12) | YES |

- **2.2.x**: Fix already present upstream. Versions 2.2.3+ ship quinn-proto 0.11.14 (the fixed version). No new upstream backport or downstream propagation needed for this stream.
- **2.1.x**: Fix NOT present upstream. The latest tag (v0.3.12) still ships quinn-proto 0.11.9. Remediation is required: upstream backport on `release/0.3.z` followed by downstream propagation in `rhtpa-release.0.3.z`.

### Affects Versions Correction (Step 3)

The issue is scoped to stream **2.2.x**. Only 2.2.x versions are included in the Affects Versions correction.

- **Current (PSIRT-assigned)**: `[RHTPA 2.0.0]`
- **Proposed (based on lock file analysis)**: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

RHTPA 2.0.0 does not correspond to any version in the supportability matrix. Versions 2.2.0, 2.2.1, and 2.2.2 are the affected versions within the 2.2.x stream. Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (the fixed version) and are NOT affected.

### Cross-Stream Impact (Case A)

The issue is scoped to 2.2.x, but the version impact analysis reveals that the **2.1.x** stream is also affected:

- 2.1.0: quinn-proto 0.11.9 -- AFFECTED
- 2.1.1: quinn-proto 0.11.9 -- AFFECTED

The 2.1.x stream requires preemptive remediation tasks (see remediation.md).
