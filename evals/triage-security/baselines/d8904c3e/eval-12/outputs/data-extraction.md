# Step 1 -- Data Extraction

## Issue: TC-8030

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-48901 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | "versions prior to the fix" (imprecise -- no specific threshold in Jira description) |
| Fixed version | "see advisory" (imprecise -- no specific version in Jira description) |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 |
| Due date | 2026-08-01 |
| Existing comments | None |

## Stream Scope Resolution

Summary suffix `[rhtpa-2.2]` maps to the **2.2.x** version stream (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

## Ecosystem Detection

The vulnerable library `h2` is a Rust crate. Based on the Ecosystem Mappings tables in the security matrix, this falls under the **Cargo** ecosystem.

- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`
- Classification: **source dependency** (2 remediation tasks per stream: upstream backport + downstream propagation)

## Deployment Context

The affected repository `rhtpa-backend` is listed in Source Repositories. No Deployment Context column is present in the Source Repositories table, so the default is `upstream`.

## Critical Data Gap

The Jira description provides **imprecise** affected version and fixed version information:
- Affected versions: "versions prior to the fix" -- no specific version threshold
- Fixed version: "see advisory" -- no specific version number

External CVE data enrichment (Step 1.5) is required to establish a precise fix threshold for version impact analysis.
