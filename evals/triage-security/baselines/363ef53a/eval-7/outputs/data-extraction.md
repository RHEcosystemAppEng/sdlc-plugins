# Step 1 -- Data Extraction for TC-8006

## Extracted Fields

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (Component label pattern: `pscomponent:`) |
| Product version (PSIRT-claimed) | [rhtpa-2.1] | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.1.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | (none found) | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | (none) | Issue comment history |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Mapped stream: **2.1.x** (matches Version Streams table row for `2.1.x` with Konflux Release Repo `git.example.com/rhtpa/rhtpa-release.0.3.z`)
- Issue stream scope: **scoped to 2.1.x only**

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo** (source dependency)
- Remediation task count per stream: **2** (upstream backport/dependency bump + downstream propagation)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.3.z`

## Deployment Context

- Affected repository: rhtpa-backend (matched from Source Repositories table)
- Deployment context: Not specified in Source Repositories table (Deployment Context column absent) -- defaults to `upstream`

## Pre-Existing Issue Links

The issue already has the following links:

| Link Type | Direction | Target Issue | Target Summary |
|-----------|-----------|-------------|----------------|
| Related | outward (TC-8006 -> TC-8001) | TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
