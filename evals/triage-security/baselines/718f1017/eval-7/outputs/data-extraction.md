# Step 1 -- Data Extraction for TC-8006

## Extracted Fields

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches Component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | [rhtpa-2.1] | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.1.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | Not available from remote links | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links (GitHub Advisory) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links (CVE Record) |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comment history |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Mapped to stream: **2.1.x** (from Version Streams table in Security Configuration)
- Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.3.z
- Local Path: /home/dev/repos/rhtpa-release.0.3.z
- Issue stream scope: **2.1.x only** (scoped issue -- Steps 3 and 4 apply only to this stream)

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Repository: backend
- Upstream Branch: `release/0.3.z`

## Issue Links (Pre-existing)

The issue already has the following links:

- **Related**: TC-8001 (CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2])
  - Link ID: 1990401
  - Type: Related
  - Direction: outward (TC-8006 -> TC-8001)

## Version Impact (from mock lock file data, scoped to 2.1.x stream)

| Version | Tag | quinn-proto version | Affected? | Notes |
|---------|-----|---------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | 0.11.9 < 0.11.14 (fix threshold) |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | 0.11.9 < 0.11.14 (fix threshold) |

All versions in the 2.1.x stream ship quinn-proto 0.11.9, which is below the fix threshold of 0.11.14. Both versions are affected.
