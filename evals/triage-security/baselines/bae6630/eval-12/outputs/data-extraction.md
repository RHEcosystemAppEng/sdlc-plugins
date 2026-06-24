# Step 1 -- Data Extraction

## Issue: TC-8030

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-48901 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | "versions prior to the fix" (imprecise -- no specific version threshold in Jira description) |
| Fixed version | "see advisory" (not specified precisely in Jira description) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 |
| CVSS | 7.5 (High) |
| Due date | 2026-08-01 |
| Existing comments | (none) |
| Status | New |
| Assignee | Unassigned |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`). This issue is **scoped** to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library is **h2**, a Rust crate (HTTP/2 implementation). Based on the Ecosystem Mappings tables in the security matrix, the ecosystem is **Cargo**. The lock file is `Cargo.lock` and the check command is `git show <tag>:Cargo.lock`.

## Additional References

- RUSTSEC: https://rustsec.org/advisories/RUSTSEC-2026-0089.html
- GHSA: https://github.com/advisories/GHSA-2026-r7f2-kk9p

## Vulnerability Description

A vulnerability was found in h2. The h2 crate is affected by an HTTP/2 CONTINUATION flood vulnerability. An attacker can send a large number of CONTINUATION frames that causes excessive memory allocation and CPU usage. The vulnerability exists because h2 does not limit the number of CONTINUATION frames that can follow a HEADERS frame. An attacker can exploit this to cause a denial of service.

## Note on Imprecise Version Data

The Jira description states affected versions are "versions prior to the fix" with no precise version threshold, and the fixed version is described as "see advisory" without a specific version number. This imprecise data necessitates external CVE data enrichment (Step 1.5) to obtain a machine-readable fix threshold for version impact analysis.
