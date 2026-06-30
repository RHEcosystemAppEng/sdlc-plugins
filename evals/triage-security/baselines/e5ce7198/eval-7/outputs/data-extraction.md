# Step 1 -- Data Extraction for TC-8006

## Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (pscomponent: pattern) |
| Product version (PSIRT-claimed) | [rhtpa-2.1] | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.1.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | N/A (not provided in remote links) | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comments |
| Issue status | New | Jira status field |
| Assignee | Unassigned | Jira assignee field |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Mapped stream: **2.1.x** (matches Version Streams table row: Stream `2.1.x`, Konflux Release Repo `git.example.com/rhtpa/rhtpa-release.0.3.z`)
- Issue stream scope: **scoped to 2.1.x only**

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.3.z`
- Source repository: backend (rhtpa-backend)

## Existing Issue Links

The following links already exist on TC-8006:

| Link Type | Direction | Linked Issue | Link ID |
|-----------|-----------|--------------|---------|
| Related | outward (TC-8006 -> TC-8001) | TC-8001 (CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]) | 1990401 |

## Version Impact (from mock lock file data, scoped to 2.1.x stream)

| Version | Tag | quinn-proto version | Affected? (< 0.11.14) | Notes |
|---------|-----|---------------------|----------------------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | 0.11.9 < 0.11.14 |

Both versions in the 2.1.x stream ship quinn-proto 0.11.9, which is within the affected range (< 0.11.14).

## Cross-stream Version Impact (informational, for other streams)

| Version | Tag | quinn-proto version | Affected? (< 0.11.14) | Notes |
|---------|-----|---------------------|----------------------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | v0.4.9 | (retag of v0.4.8) | YES | same as 2.2.1 |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | ships fixed version |

The 2.2.x stream is tracked by sibling issue TC-8001 (status: In Progress).
