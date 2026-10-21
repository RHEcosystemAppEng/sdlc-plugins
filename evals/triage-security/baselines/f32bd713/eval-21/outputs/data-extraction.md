# Step 1 -- Data Extraction for TC-8020

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels (`CVE-2026-31812`) and summary text |
| Affected component | pscomponent:org/rhtpa-server | Label matching component label pattern `pscomponent:` |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links (quinn-rs/quinn#2048) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links (GitHub Advisory) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links (CVE Record) |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comment history |
| Upstream Affected Component | quinn-proto | customfield_10632 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry for `2.2.x` at `git.example.com/rhtpa/rhtpa-release.0.4.z`)
- Issue stream scope: **Scoped to 2.2.x**

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Detected ecosystem: **Cargo**
- Category: Source dependency
- Remediation task structure: 2 tasks per stream (upstream backport or dependency bump + downstream propagation)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z` (for 2.2.x stream)

## Deployment Context Lookup

- Affected repository from component label `pscomponent:org/rhtpa-server`: rhtpa-backend
- Deployment context: `upstream` (from Source Repositories table)

## Affects Versions Discrepancy

PSIRT assigned Affects Versions as **RHTPA 2.0.0**. There is no 2.0.x version stream configured in Security Configuration. The Version Streams table defines only 2.1.x and 2.2.x. The PSIRT-assigned version is incorrect and requires correction in Step 3.

## Version Impact Analysis (Step 2)

### 2.2.x Stream (issue scope)

| Version | Build Tag | quinn-proto version | Affected (< 0.11.14)? |
|---------|-----------|---------------------|------------------------|
| 2.2.0 | v0.4.5 | 0.11.9 | **YES** |
| 2.2.1 | v0.4.8 | 0.11.12 | **YES** |
| 2.2.2 | v0.4.9 | 0.11.12 (retag of v0.4.8) | **YES** (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.11.14 | **NO** (= fix version) |
| 2.2.4 | v0.4.12 | 0.11.14 | **NO** (= fix version) |

### 2.1.x Stream (cross-stream check)

| Version | Build Tag | quinn-proto version | Affected (< 0.11.14)? |
|---------|-----------|---------------------|------------------------|
| 2.1.0 | v0.3.8 | 0.11.9 | **YES** |
| 2.1.1 | v0.3.12 | 0.11.9 | **YES** |

### Summary

- **2.2.x stream**: Versions 2.2.0, 2.2.1, 2.2.2 are affected. Versions 2.2.3, 2.2.4 are NOT affected (they ship quinn-proto 0.11.14, the fixed version).
- **2.1.x stream**: Both versions 2.1.0 and 2.1.1 are affected. This is a cross-stream impact that triggers Case A (the issue is scoped to 2.2.x but 2.1.x is also affected).

## Step 1.5 -- External CVE Data Enrichment

External sources (MITRE CVE API and OSV.dev) would be queried for CVE-2026-31812 to cross-validate the fix threshold of 0.11.14. Since we are not calling external services:

- MITRE CVE API: Would query `https://cveawg.mitre.org/api/cve/CVE-2026-31812`
- OSV.dev API: Would query `https://api.osv.dev/v1/vulns/CVE-2026-31812`

The Jira description data is used as the authoritative source:
- Affected range: < 0.11.14
- Fixed version: 0.11.14

## Step 1.7 -- Embargo Check

- Embargo policy URL: Not configured in Security Configuration
- Action: **Skip** -- Step 1.7 is skipped entirely when no embargo policy URL is configured.
