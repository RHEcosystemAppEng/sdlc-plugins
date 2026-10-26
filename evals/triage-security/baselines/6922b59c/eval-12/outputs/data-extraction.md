# Step 1 -- Data Extraction

## Issue: TC-8030

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-48901 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | versions prior to the fix (imprecise -- no explicit threshold in Jira description) |
| Fixed version | see advisory (imprecise -- no explicit version in Jira description) |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 |
| Due date | 2026-08-01 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration Version Streams table:

| Stream | Konflux Release Repo |
|--------|----------------------|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z |

**Issue stream scope**: 2.2.x (scoped issue -- only the 2.2.x stream is in scope for Steps 3-8, but all streams are analyzed in Step 2 for cross-stream impact).

## Ecosystem Detection

The vulnerable library `h2` is a Rust crate found in `Cargo.lock`. This maps to the **Cargo** ecosystem in the Ecosystem Mappings table.

- **Ecosystem**: Cargo
- **Category**: Source dependency
- **Lock File**: `Cargo.lock`
- **Check Command**: `git show <tag>:Cargo.lock`
- **Remediation tasks per stream**: 2 (upstream backport/dependency bump + downstream propagation)

## Deployment Context

The affected repository `rhtpa-backend` has deployment context: **upstream** (default, as no explicit Deployment Context column is present in the Source Repositories table).

## Imprecise Jira Description

The Jira description does not provide a precise affected version range or fixed version:
- Affected versions: "versions prior to the fix" (no version number)
- Fixed version: "see advisory" (no version number)

External CVE data enrichment (Step 1.5) is required to determine the precise fix threshold.
