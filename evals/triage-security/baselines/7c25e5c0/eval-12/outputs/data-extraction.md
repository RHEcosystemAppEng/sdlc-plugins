# Step 1 — Data Extraction for TC-8030

## Step 0.7 — Early Assignment

- **Action**: Assign TC-8030 to current user
- **Action**: Transition TC-8030 from New → Assigned

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-48901 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | versions prior to the fix *(imprecise — no specific version threshold provided in the Jira description)* |
| Fixed version | see advisory *(imprecise — no specific version provided in the Jira description)* |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 |
| Due date | 2026-08-01 |
| CVSS | 7.5 (High) |
| Existing comments | None |

## Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]` → scoped to **2.2.x** stream.

## Ecosystem Detection

Library `h2` is a Rust crate. The 2.2.x stream's Ecosystem Mappings table lists **Cargo** as a supported ecosystem with lock file `Cargo.lock` and check command `git show <tag>:Cargo.lock`.

Ecosystem: **Cargo** (source dependency)

## Note on Imprecise Data

The Jira description provides only "versions prior to the fix" and "see advisory" — no specific version threshold. Step 1.5 (External CVE Data Enrichment) is required to obtain a precise fix threshold for version impact analysis.
