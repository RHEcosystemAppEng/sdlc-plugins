# Step 1 -- Data Extraction for TC-8003

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| Upstream fix PR | Not provided in remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| CVSS | 7.5 (High) |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`.

1. Parsed suffix: `rhtpa-2.2` maps to stream **2.2.x**
2. Matched to Version Streams table: stream `2.2.x` is configured with Konflux Release Repo `git.example.com/rhtpa/rhtpa-release.0.4.z`
3. Issue stream scope: **2.2.x only**

This is a **scoped** issue -- Steps 3 and 4 apply only to the 2.2.x stream.

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. This maps to the **Cargo** ecosystem.

From the 2.2.x stream's Ecosystem Mappings:
- Ecosystem: Cargo
- Repository: backend
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`

## Version Impact Analysis (Step 2)

Using mock lock file data from the security matrix, the quinn-proto versions by tag are:

### 2.2.x Stream (in scope)

| Version | Tag | quinn-proto version | Affected? (< 0.11.14) | Notes |
|---------|-----|---------------------|----------------------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8 = 0.11.12) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | ships the fixed version |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | ships the fixed version |

### 2.1.x Stream (out of scope for this issue, included for cross-stream awareness)

| Version | Tag | quinn-proto version | Affected? (< 0.11.14) | Notes |
|---------|-----|---------------------|----------------------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | |

## Configuration Validation (Step 0)

Confirmed from claude-md-security-config.md:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Jira version prefix: RHTPA
- Vulnerability issue type ID: 10024
- Product pages URL: https://access.example.com/product-life-cycle/rhtpa
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345
- Version Streams: 2.1.x, 2.2.x
- Source Repositories: rhtpa-backend (https://github.com/rhtpa/rhtpa-backend)
