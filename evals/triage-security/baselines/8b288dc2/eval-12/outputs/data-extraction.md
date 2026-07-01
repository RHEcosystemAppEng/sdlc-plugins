# Step 1 -- Data Extraction: TC-8030

## Extracted Fields

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-48901 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0 | Jira `versions` field |
| Vulnerable library | h2 | Description text |
| Affected version range | versions prior to the fix (imprecise) | Description text |
| Fixed version | see advisory (imprecise) | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | [hyperium/h2#800](https://github.com/hyperium/h2/pull/800) | Remote links |
| Advisory URL | [GHSA-2026-r7f2-kk9p](https://github.com/advisories/GHSA-2026-r7f2-kk9p) | Remote links |
| CVE record URL | [CVE-2026-48901](https://www.cve.org/CVERecord?id=CVE-2026-48901) | Remote links |
| Due date | 2026-08-01 | Issue `duedate` field |
| Existing comments | None | Issue comment history |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table row for `2.2.x` backed by `rhtpa-release.0.4.z`)
- Issue is **stream-scoped** to 2.2.x only

## Ecosystem Detection

- Vulnerable library: h2 (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- This is a source dependency ecosystem, so remediation produces 2 tasks (upstream backport + downstream propagation)

## Deployment Context Lookup

- Affected repository: rhtpa-backend (mapped from component label `pscomponent:org/rhtpa-server`)
- Source Repositories table does **not** include a Deployment Context column
- Default deployment context: **upstream** (backward compatibility default)
- Coordination guidance: **omitted** (Deployment Context column absent)

## Data Quality Notes

- **Affected version range** is imprecise: "versions prior to the fix" -- no specific version threshold provided in the Jira description
- **Fixed version** is imprecise: "see advisory" -- no specific version number in the Jira description
- External CVE data enrichment (Step 1.5) is required to establish a precise fix threshold for version impact analysis
