# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-45678 |
| Affected component | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | webpack |
| Affected version range | versions before 5.98.0 (< 5.98.0) |
| Fixed version | 5.98.0 |
| CVSS | 7.8 (High) |
| Upstream fix PR | Not provided in remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 |
| Due date | 2026-08-15 |
| Existing comments | None |
| Upstream Affected Component (customfield_10632) | webpack |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-ui |
| Stream (customfield_10832) | rhtpa-2.2 |
| Issue links | None (no existing links) |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. This maps to the **2.2.x** stream in the Version Streams table from Security Configuration:

- Stream suffix: `[rhtpa-2.2]` --> stream `2.2.x`
- Konflux Release Repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Local Path: `/home/dev/repos/rhtpa-release.0.4.z`

**Issue stream scope**: 2.2.x only.

## Ecosystem Detection

The vulnerable library is **webpack**, which is a JavaScript/TypeScript package (npm ecosystem).

Checking the stream's `security-matrix.md` Ecosystem Mappings table for the 2.2.x stream:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

The npm ecosystem is **not** listed in the Ecosystem Mappings table for this stream. However, webpack is clearly an npm package. The triage will proceed through Step 4.3 (cross-CVE overlap detection) before determining whether version impact analysis and remediation task creation are needed, since the overlap check may resolve the issue without requiring ecosystem-specific lock file inspection.

## Deployment Context Lookup

The Source Repositories table in Security Configuration does not have a Deployment Context column. Per backward compatibility rules, all repositories default to `upstream`.
