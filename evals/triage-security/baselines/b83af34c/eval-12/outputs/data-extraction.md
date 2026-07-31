# Step 1 -- Data Extraction

## Issue: TC-8030

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-48901 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | **Imprecise** -- "versions prior to the fix" (no specific version threshold provided in the Jira description) |
| Fixed version | **Imprecise** -- "see advisory" (no specific fixed version provided in the Jira description) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 |
| Due date | 2026-08-01 |
| Existing comments | None |
| CVSS | 7.5 (High) |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Issue stream scope: **2.2.x only**

## Ecosystem Detection

- Library: h2 (Rust crate)
- Ecosystem: **Cargo** (source dependency)
- Remediation tasks per stream: 2 (upstream backport + downstream propagation)

## Data Quality Note

The Jira description does **not** provide a precise affected version range or fixed version. The description states:
- **Affected versions**: "versions prior to the fix" -- this is a vague prose statement with no specific version threshold
- **Fixed version**: "see advisory" -- delegates to external references without stating the version

This imprecise data is insufficient for Step 2.3 version impact comparison. External CVE data enrichment (Step 1.5) is required to obtain a machine-readable fix threshold.
