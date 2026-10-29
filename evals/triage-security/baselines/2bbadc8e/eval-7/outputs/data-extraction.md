# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches `pscomponent:` pattern from Security Configuration) |
| Product version (PSIRT-claimed) | [rhtpa-2.1] | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.1.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description |
| Affected version range | versions before 0.11.14 | Description |
| Fixed version | 0.11.14 | Description |
| CVSS | 7.5 (High) | Description |
| Upstream fix PR | (none found) | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Jira `duedate` field |
| Existing comments | (none) | Issue comments |
| Assignee | Unassigned | Jira `assignee` field |
| Status | New | Jira `status` field |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Parsed stream: `2.1.x`
- Matched Version Stream: `2.1.x` (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.3.z`, local path: `/home/dev/repos/rhtpa-release.0.3.z`)
- Issue stream scope: **2.1.x only**

The issue is **stream-scoped** to 2.1.x. Steps 3 and 4 will apply only to versions in the 2.1.x stream.

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Category: Source dependency
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.3.z`

Per the ecosystem classification table, Cargo is a source dependency ecosystem. Remediation produces 2 tasks per affected stream: upstream backport (or dependency bump if fix is already upstream) + downstream propagation.

## Deployment Context Lookup

- Affected repository: rhtpa-backend (from component label `pscomponent:org/rhtpa-server`)
- Source Repositories match: rhtpa-backend (URL: https://github.com/rhtpa/rhtpa-backend, local path: /home/dev/repos/rhtpa-backend)
- Deployment context: `upstream` (default -- no Deployment Context column present in configuration)

## Existing Issue Links

The issue already has the following links:

| Link Type | Direction | Target | Target Summary |
|-----------|-----------|--------|----------------|
| Related | outward (TC-8006 -> TC-8001) | TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |

Link ID: 1990401
