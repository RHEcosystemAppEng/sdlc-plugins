# Step 1 -- Data Extraction for TC-8006

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches Component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | [rhtpa-2.1] | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.1.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | (none found in remote links) | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links (GitHub Advisory) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links (cve.org) |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comment history |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Parsed stream: `2.1.x`
- Matched to Version Streams table: **2.1.x** (Konflux Release Repo: `git.example.com/rhtpa/rhtpa-release.0.3.z`)
- Issue stream scope: **2.1.x** (scoped issue -- Steps 3-4 apply only to this stream)

## Ecosystem Detection

- Vulnerable library: quinn-proto (Rust crate)
- Detected ecosystem: **Cargo**
- Category: Source dependency
- Remediation tasks per stream: 2 (upstream backport/dependency bump + downstream propagation)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.3.z`

## Deployment Context Lookup

- Affected repository: rhtpa-backend (derived from component label `pscomponent:org/rhtpa-server`)
- Source Repositories table lookup: rhtpa-backend found at https://github.com/rhtpa/rhtpa-backend
- Deployment Context column: **absent** from the Source Repositories table (only Repository, URL, Local Path columns are present)
- Deployment context: defaults to `upstream` (per backward compatibility rule)

## Existing Issue Links

The issue has the following pre-existing links:

| Link Type | Direction | Linked Issue | Linked Issue Summary |
|-----------|-----------|-------------|---------------------|
| Related | outward (TC-8006 -> TC-8001) | TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
