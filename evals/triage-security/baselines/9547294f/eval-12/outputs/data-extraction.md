# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-48901 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0 | Jira `versions` field |
| Vulnerable library | h2 | Description text |
| Affected version range | "versions prior to the fix" (imprecise -- no specific threshold) | Description text |
| Fixed version | "see advisory" (imprecise -- no specific version) | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 | Remote links |
| Due date | 2026-08-01 | Jira `duedate` field |
| Existing comments | None | Issue comments |

## Stream Scope

Issue summary contains stream suffix `[rhtpa-2.2]` which maps to the **2.2.x** stream (Konflux release repo: rhtpa-release.0.4.z).

Triage is scoped to the 2.2.x stream.

## Ecosystem Detection

The vulnerable library **h2** is a Rust crate (HTTP/2 implementation for Rust). Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, the ecosystem is **Cargo**.

- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`

## Imprecise Version Data

The Jira description does **not** contain a precise fix threshold:
- Affected versions field says: "versions prior to the fix" -- this is imprecise with no specific version number
- Fixed version field says: "see advisory" -- this refers to an external advisory without stating the version

This imprecise data is insufficient for version impact comparisons. Step 1.5 (External CVE Data Enrichment) is required to obtain a precise fix threshold from external sources.
