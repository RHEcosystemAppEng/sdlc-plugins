# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-48901 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0 | Jira `versions` field |
| Vulnerable library | h2 | Description text |
| Affected version range | "versions prior to the fix" (imprecise) | Description text |
| Fixed version | "see advisory" (imprecise) | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | [hyperium/h2#800](https://github.com/hyperium/h2/pull/800) | Remote links |
| Advisory URL | [GHSA-2026-r7f2-kk9p](https://github.com/advisories/GHSA-2026-r7f2-kk9p) | Remote links |
| CVE record URL | [CVE-2026-48901](https://www.cve.org/CVERecord?id=CVE-2026-48901) | Remote links |
| Due date | 2026-08-01 | Jira `duedate` field |
| Existing comments | None | Issue comment history |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams table. Triage is scoped to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library **h2** is a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's `security-matrix.md`, this maps to the **Cargo** ecosystem.

- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`

## Imprecise Version Data

The Jira description provides only imprecise affected version information:

- **Affected versions**: "versions prior to the fix" -- no specific version threshold
- **Fixed version**: "see advisory" -- no explicit version number

These values are insufficient for version impact analysis. Step 1.5 (External CVE Data Enrichment) is required to obtain a precise fix threshold.
