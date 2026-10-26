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
| Existing comments | (none) |

### Stream Scope Resolution

Issue summary contains `[rhtpa-2.2]` --> maps to stream **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`). This is a **scoped** issue.

### Ecosystem Detection

- **Ecosystem**: Cargo (quinn-proto is a Rust crate)
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`
- **Category**: Source dependency
- **Tasks per stream**: 2 (dependency bump + downstream propagation when fix available upstream; upstream backport + downstream propagation when not)

### Deployment Context

The Source Repositories table does **not** have a Deployment Context column. Per backward compatibility rules, coordination guidance is omitted entirely from remediation task descriptions.

### Source Repository Mapping

| Repository | URL | Local Path |
|------------|-----|------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend |

## Step 2 -- Version Impact Analysis

### Supportability Matrix (aggregated from all streams)

**Stream 2.1.x** (rhtpa-release.0.3.z):

| Version | Build | Build Date | backend tag |
|---------|-------|------------|-------------|
| 2.1.0 | 0.3.8 | 2025-09-15 | v0.3.8 |
| 2.1.1 | 0.3.12 | 2025-11-20 | v0.3.12 |

**Stream 2.2.x** (rhtpa-release.0.4.z):

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 | |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 | |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 | |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 | |

### Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | ships fixed version |

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Latest Tag | Version at Tag | Fixed? |
|--------|-----------|-----------------|------------|----------------|--------|
| 2.1.x | Cargo | release/0.3.z | v0.3.12 | 0.11.9 | NO |
| 2.2.x | Cargo | release/0.4.z | v0.4.12 | 0.11.14 | YES |

### Step 3 -- Affects Versions Correction

Issue is scoped to stream 2.2.x. Only versions from the 2.2.x stream are in scope.

- **Current Affects Versions**: `[RHTPA 2.0.0]` (incorrect -- RHTPA 2.0.0 is not a valid version in any configured stream)
- **Corrected Affects Versions**: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]` (based on lock file evidence at pinned commits)

### Step 4 -- Duplicate/Sibling Check

No sibling Vulnerability issues found for CVE-2026-31812 (no other issues with the CVE-2026-31812 label exist in the project).

### Steps 5-7

- **Step 5 (Lifecycle)**: Skipped in eval mode (no external service access).
- **Step 6 (Already Fixed)**: No resolved siblings found -- proceed to remediation.
- **Step 7 (Concurrent Triage)**: Skipped -- no Upstream Affected Component custom field configured.

### Case A: Cross-Stream Impact

This issue is scoped to 2.2.x, but the version impact analysis reveals that **stream 2.1.x** is also affected (all versions: 2.1.0, 2.1.1). No sibling CVE Jira exists for 2.1.x.

**Cross-stream impact comment**:
> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. This stream is not tracked by a companion issue and may require separate PSIRT triage.

Preemptive remediation tasks will be created for stream 2.1.x (see remediation.md).

### Case B: Remediation Required

For the scoped stream 2.2.x:
- Affected versions: 2.2.0, 2.2.1, 2.2.2
- Upstream fix is available on release/0.4.z (v0.4.11+ ships 0.11.14)
- Remediation type: **dependency bump** + **downstream propagation** (2 tasks)

For the cross-stream 2.1.x (preemptive):
- Affected versions: 2.1.0, 2.1.1
- Upstream fix is NOT available on release/0.3.z (v0.3.12 still ships 0.11.9)
- Remediation type: **upstream backport** + **downstream propagation** (2 preemptive tasks)
