# Step 1 -- Data Extraction: TC-8003

## Parsed Fields

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| Upstream fix PR | (none found in remote links) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| CVSS | 7.5 (High) |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry for `rhtpa-release.0.4.z`)
- Issue stream scope: **scoped to 2.2.x only**

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`
- Source repository: rhtpa-backend

## Version Impact Analysis (from mock lock file data)

Using the security-matrix.md Supportability Matrix for the 2.2.x stream (`rhtpa-release.0.4.z`), the quinn-proto versions at each pinned commit are:

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.2.0   | v0.4.5    | 0.11.9              | YES       | < 0.11.14 |
| 2.2.1   | v0.4.8    | 0.11.12             | YES       | < 0.11.14 |
| 2.2.2   | v0.4.9    | --                  | YES       | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3   | v0.4.11   | 0.11.14             | NO        | >= 0.11.14 (fixed) |
| 2.2.4   | v0.4.12   | 0.11.14             | NO        | >= 0.11.14 (fixed) |

The 2.1.x stream (rhtpa-release.0.3.z) is outside the issue's scope but also affected:

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.1.0   | v0.3.8    | 0.11.9              | YES       | < 0.11.14 |
| 2.1.1   | v0.3.12   | 0.11.9              | YES       | < 0.11.14 |
