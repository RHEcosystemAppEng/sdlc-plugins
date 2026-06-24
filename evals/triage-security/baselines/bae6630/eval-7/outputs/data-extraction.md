# Step 1 -- Data Extraction for TC-8006

## Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels (`CVE-2026-31812`) and summary text |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches `pscomponent:` pattern from Security Configuration) |
| Product version (PSIRT-claimed) | [rhtpa-2.1] | Summary suffix in brackets |
| Affects Versions (Jira field) | RHTPA 2.1.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text ("A vulnerability was found in quinn-proto") |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text ("Fixed version: 0.11.14") |
| CVSS | 7.5 (High) | Description text |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links (GitHub Advisory) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links (CVE Record) |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comment history |
| Assignee | Unassigned | Issue field |
| Status | New | Issue field |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Parsed stream: `2.1.x`
- Matched Version Stream: `2.1.x` (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.3.z`, local path: `/home/dev/repos/rhtpa-release.0.3.z`)
- Issue stream scope: **2.1.x only** (scoped issue -- Steps 3-4 apply only to this stream)

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.3.z`
- Source repository: backend (rhtpa-backend)

## Existing Issue Links

The issue already has the following links (from `issuelinks` array in the `jira.get_issue` response):

| Link ID | Type | Direction | Target Issue |
|---------|------|-----------|--------------|
| 1990401 | Related | outward (TC-8006 -> TC-8001) | TC-8001 (CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]) |

## Version Impact (from security-matrix mock data)

Using the 2.1.x stream's supportability matrix (stream rhtpa-release.0.3.z):

| Version | Build Tag | quinn-proto version | Affected? (< 0.11.14) | Notes |
|---------|-----------|---------------------|------------------------|-------|
| 2.1.0   | v0.3.8    | 0.11.9              | YES                    |       |
| 2.1.1   | v0.3.12   | 0.11.9              | YES                    |       |

Cross-stream reference (2.2.x stream, rhtpa-release.0.4.z -- for context, not in scope for this issue):

| Version | Build Tag | quinn-proto version | Affected? (< 0.11.14) | Notes |
|---------|-----------|---------------------|------------------------|-------|
| 2.2.0   | v0.4.5    | 0.11.9              | YES                    |       |
| 2.2.1   | v0.4.8    | 0.11.12             | YES                    |       |
| 2.2.2   | v0.4.9    | --                  | YES                    | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3   | v0.4.11   | 0.11.14             | NO                     | Fixed |
| 2.2.4   | v0.4.12   | 0.11.14             | NO                     | Fixed |
