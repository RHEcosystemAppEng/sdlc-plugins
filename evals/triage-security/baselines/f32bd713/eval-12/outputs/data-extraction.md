# Step 1 -- Data Extraction

## Issue: TC-8030

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-48901 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | "versions prior to the fix" (imprecise -- no explicit version threshold in Jira description) |
| Fixed version | "see advisory" (imprecise -- no explicit version in Jira description) |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 |
| Due date | 2026-08-01 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration Version Streams table.

- Stream suffix parsed: `rhtpa-2.2` --> stream `2.2.x`
- Matched Version Stream: 2.2.x (Konflux release repo: `rhtpa-release.0.4.z`)
- Issue stream scope: **2.2.x only**

## Ecosystem Detection

- Library: h2
- Ecosystem: **Cargo** (Rust crate, identified from crates.io ecosystem context)
- Category: Source dependency
- Remediation tasks per stream: 2 (upstream backport/dependency bump + downstream propagation)

## Deployment Context

- Repository: rhtpa-backend
- Deployment context: **upstream** (default -- Deployment Context column absent from Source Repositories table)

## Critical Finding: Imprecise Jira Description

The Jira description does not provide a precise affected version range or fixed version:
- Affected versions: "versions prior to the fix" -- no version number
- Fixed version: "see advisory" -- no version number

External CVE data enrichment (Step 1.5) is required to establish a usable fix threshold for version impact analysis.
