# Step 1 -- Data Extraction for TC-8006

## Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches `pscomponent:` pattern from Security Configuration) |
| Product version (PSIRT-claimed) | [rhtpa-2.1] | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.1.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description |
| Fixed version | 0.11.14 | Description |
| CVSS | 7.5 (High) | Description |
| Upstream fix PR | (none found in remote links) | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | (none) | Issue comments |
| Assignee | Unassigned | Issue field |
| Status | New | Issue field |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Parsed stream: `2.1.x`
- Matched Version Stream: `2.1.x` (Konflux Release Repo: `git.example.com/rhtpa/rhtpa-release.0.3.z`, Local Path: `/home/dev/repos/rhtpa-release.0.3.z`)
- Issue stream scope: **2.1.x only**

Since the issue is scoped to the 2.1.x stream, Steps 3 and 4 will only apply Affects Versions for versions in that stream. Other streams are tracked by sibling/companion issues.

## Ecosystem Detection

- Vulnerable library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
- Upstream branch: `release/0.3.z` (for stream 2.1.x)

## Existing Issue Links

The issue already has the following links:

| Link Type | Direction | Target Issue | Target Summary |
|-----------|-----------|--------------|----------------|
| Related | outward (TC-8006 -> TC-8001) | TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |

## Version Impact Analysis (Step 2)

Using the mock lock file data from the security matrix, the version impact for stream 2.1.x is:

| Version | Tag | quinn-proto version | Affected? | Notes |
|---------|-----|---------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | 0.11.9 < 0.11.14 (fix threshold) |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | 0.11.9 < 0.11.14 (fix threshold) |

Cross-stream versions (for context, scoped to sibling TC-8001):

| Version | Tag | quinn-proto version | Affected? | Notes |
|---------|-----|---------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.2 | v0.4.9 | (retag of v0.4.8) | YES | same as 2.2.1 |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |

All versions in the 2.1.x stream ship quinn-proto 0.11.9, which is below the fix threshold of 0.11.14. Both RHTPA 2.1.0 and RHTPA 2.1.1 are affected.
