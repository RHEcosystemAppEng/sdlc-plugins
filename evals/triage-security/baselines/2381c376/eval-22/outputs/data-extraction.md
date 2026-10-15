# Step 1 -- Data Extraction for TC-8021

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| RustSec advisory | https://rustsec.org/advisories/RUSTSEC-2026-0042.html | Description references |
| Due date | 2026-07-15 | Jira `duedate` field |
| Upstream Affected Component | quinn-proto | customfield_10632 |
| Existing comments | None | Issue comment history |

## Stream Scope Resolution

- Summary contains stream suffix: `[rhtpa-2.2]`
- Mapped to configured Version Stream: **2.2.x** (Konflux release repo: rhtpa-release.0.4.z)
- Issue is **scoped** to stream 2.2.x only
- Other streams (2.1.x) will be analyzed but remediation scoping follows Case A/B rules

## Ecosystem Detection

- Vulnerable library: quinn-proto (Rust crate)
- Detected ecosystem: **Cargo**
- Category: Source dependency
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Remediation tasks per stream: 2 (upstream fix + downstream propagation)

## Deployment Context

- Affected repository: rhtpa-backend
- Source Repositories lookup: rhtpa-backend -> URL: https://github.com/rhtpa/rhtpa-backend
- Deployment context: **upstream** (default -- no Deployment Context column configured)

## Configuration Extracted (Step 0)

| Parameter | Value |
|-----------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component custom field | customfield_10632 |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend (https://github.com/rhtpa/rhtpa-backend) |

## Step 0.3 -- Matrix Staleness Check

- Matrix `Last-Updated` timestamp: `2026-06-28T10:00:00Z`
- Current date (simulated): 2026-10-15
- Staleness: approximately 109 days old -- exceeds 14-day threshold
- In a live triage, the engineer would be warned and offered a choice to refresh, proceed, or stop
- For this eval: proceeding with the current matrix data

## Version Impact Analysis (Step 2)

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | >= 0.11.14 (fixed) |

### Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Latest Tag Version | Fixed? |
|--------|-----------|-----------------|---------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (v0.4.12) | YES |

- Stream 2.2.x: the upstream branch `release/0.4.z` already ships quinn-proto 0.11.14 (confirmed by v0.4.11 and v0.4.12 tags). Remediation for 2.2.x uses the **dependency bump** variant (cargo update) rather than upstream backport.
- Stream 2.1.x: the upstream branch `release/0.3.z` still ships quinn-proto 0.11.9. Remediation for 2.1.x would require an **upstream backport** to bump the dependency on the release/0.3.z branch.

### Affects Versions Correction (Step 3)

- Current Affects Versions: `[RHTPA 2.0.0]`
- RHTPA 2.0.0 does not correspond to any configured version stream -- this is incorrect
- Issue is scoped to stream 2.2.x, so only 2.2.x affected versions should be included
- Affected 2.2.x versions: 2.2.0, 2.2.1, 2.2.2
- Proposed correction: `[RHTPA 2.0.0]` -> `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
