# Step 1 -- Data Extraction

## Issue: TC-8006

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.1 (from summary suffix `[rhtpa-2.1]`) |
| Affects Versions (Jira field) | RHTPA 2.1.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| Upstream fix PR | (none found in remote links) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | (none) |
| CVSS | 7.5 (High) |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Mapped stream: **2.1.x** (Konflux release repo: `rhtpa-release.0.3.z`)
- Issue stream scope: **2.1.x only**

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Source repository: rhtpa-backend
- Upstream branch: `release/0.3.z`

## Existing Issue Links

- **Related** (outward): TC-8001 -- CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] (Link ID: 1990401)

## Version Impact (from mock lock file data)

Scoped to stream 2.1.x:

| Version | Build Tag | quinn-proto version | Affected? (< 0.11.14) |
|---------|-----------|---------------------|------------------------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES |
| 2.1.1 | v0.3.12 | 0.11.9 | YES |

Cross-stream reference (2.2.x -- tracked by sibling TC-8001):

| Version | Build Tag | quinn-proto version | Affected? (< 0.11.14) |
|---------|-----------|---------------------|------------------------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES |
| 2.2.1 | v0.4.8 | 0.11.12 | YES |
| 2.2.2 | v0.4.9 | _(retag of v0.4.8)_ | YES (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO (fixed) |
