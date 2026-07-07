# Step 1 — Data Extraction

## Issue: TC-8030

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-48901 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels |
| Product version (PSIRT-claimed) | [rhtpa-2.2] | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | Jira `versions` field |
| Vulnerable library | h2 | Description |
| Affected version range | "versions prior to the fix" (imprecise) | Description |
| Fixed version | "see advisory" (imprecise) | Description |
| CVSS | 7.5 (High) | Description |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 | Remote links |
| Due date | 2026-08-01 | Jira `duedate` field |
| Existing comments | None | Issue comment history |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Issue stream scope: **scoped to 2.2.x only**

## Ecosystem Detection

- Vulnerable library: h2 (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`
- Upstream branch: `release/0.4.z` (for 2.2.x stream)

## Deployment Context Lookup

- Component label: `pscomponent:org/rhtpa-server`
- Source repository: rhtpa-backend
- Deployment context: **upstream** (default — no Deployment Context column configured)

## Data Quality Flags

The Jira description provides **imprecise version data**:
- Affected version range says "versions prior to the fix" — no specific version threshold
- Fixed version says "see advisory" — no specific version number

External CVE data enrichment (Step 1.5) is required to obtain precise fix thresholds for version impact analysis.
