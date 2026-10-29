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

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the configured Version Stream **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`). This issue is **scoped** to the 2.2.x stream.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. From the Ecosystem Mappings tables in both streams' security matrices:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` (2.1.x) / `release/0.4.z` (2.2.x) |

Classification: **Source dependency** ecosystem (Cargo) -- produces 2 remediation tasks per affected stream (dependency bump + downstream propagation, since the upstream fix is already available).

## Deployment Context Lookup

The affected component label `pscomponent:org/rhtpa-server` maps to the source repository **rhtpa-backend** in the Source Repositories table.

| Repository | URL | Local Path | Deployment Context |
|------------|-----|------------|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | **customer-shipped** |

Deployment context for rhtpa-backend: **customer-shipped**

This deployment context will be used in Step 8 (Remediation) to generate coordination guidance in remediation task descriptions. The `customer-shipped` context requires coordination with Product Security for CVE assignment, advisory preparation, and formal disclosure.

## Step 2 -- Version Impact Analysis

### Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Build Tag | quinn-proto | Affected? | Notes |
|--------|---------|-----------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.9 | 0.11.12 | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | ships fixed version |

### Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: source dependency (Cargo crate)
  Ecosystem: Cargo
  Lock file: Cargo.lock
```

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Latest Tag | quinn-proto at HEAD | Fixed? |
|--------|-----------|-----------------|------------|---------------------|--------|
| 2.1.x | Cargo | release/0.3.z | v0.3.12 | 0.11.9 | NO |
| 2.2.x | Cargo | release/0.4.z | v0.4.12 | 0.11.14 | YES |

- **2.2.x stream**: Fix is available upstream (v0.4.11+ ships quinn-proto 0.11.14). Remediation is a dependency bump + downstream propagation.
- **2.1.x stream**: Fix is NOT yet available on the release/0.3.z branch (latest v0.3.12 ships quinn-proto 0.11.9). Remediation requires an upstream backport + downstream propagation.

### Affects Versions Correction (Step 3)

PROPOSAL: The current Affects Versions field is set to **RHTPA 2.0.0**, which is incorrect. Based on version impact analysis, the affected versions within the scoped 2.2.x stream are:

- RHTPA 2.2.0
- RHTPA 2.2.1
- RHTPA 2.2.2

Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (the fixed version) and are NOT affected.

PROPOSAL: Remove RHTPA 2.0.0 from Affects Versions and add RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2.

### Cross-Stream Impact (Case A)

This issue is scoped to stream 2.2.x, but the version impact analysis reveals that stream **2.1.x** is also affected (both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9, which is within the vulnerable range).

Cross-stream impact comment (PROPOSAL):
> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. Both versions (2.1.0 and 2.1.1) ship quinn-proto 0.11.9. This stream is tracked by companion issues (see Related links) or may require separate PSIRT triage.

Preemptive remediation tasks will be created for the 2.1.x stream (see remediation.md).
