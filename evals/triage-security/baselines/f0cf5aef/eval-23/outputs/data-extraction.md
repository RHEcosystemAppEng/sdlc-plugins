# Step 0 -- Project Configuration

| Config Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories and Deployment Context

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | customer-shipped |

---

# Step 1 -- Data Extraction (TC-8001)

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
| Existing comments | (none) |

### Stream Scope Resolution

Summary suffix `[rhtpa-2.2]` maps to configured stream **2.2.x** (Konflux release repo `rhtpa-release.0.4.z`). This is a **scoped** issue -- Steps 3-4 apply to the 2.2.x stream only.

### Ecosystem Detection

Library `quinn-proto` is a Rust crate. Ecosystem: **Cargo** (source dependency). Per the ecosystem classification table, this produces **2 tasks per affected stream** (upstream backport + downstream propagation).

### Deployment Context Lookup

The affected component label `pscomponent:org/rhtpa-server` maps to repository **rhtpa-backend** in the Source Repositories table. Deployment context: **customer-shipped**.

This deployment context will be used in Step 8 (Remediation) to generate coordination guidance in each remediation task description.

---

# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Stream | Version | Backend Tag | quinn-proto | Affected? | Notes |
|--------|---------|-------------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | fixed version |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | fixed version |

### Affects Versions Correction

The PSIRT-assigned Affects Versions field is **RHTPA 2.0.0**, which does not correspond to any configured version stream. The correct Affects Versions based on lock file evidence (for the scoped stream 2.2.x) are: **RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2**.

### Cross-Stream Impact (Case A)

This issue is scoped to stream 2.2.x, but version impact analysis reveals that stream **2.1.x** is also affected (versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9). This triggers Case A: cross-stream impact with proactive remediation task creation for the 2.1.x stream.

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD (latest tag) | Fixed? |
|--------|-----------|-----------------|------------------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (v0.4.12) | YES |

For the 2.2.x stream, the fix is already present at the latest tag (v0.4.11+). Remediation is a downstream propagation to update the Konflux release repo source pinning. However, versions 2.2.0-2.2.2 shipped the vulnerable version.

For the 2.1.x stream, the fix is NOT yet present on the upstream branch -- remediation requires an upstream backport PR first.
