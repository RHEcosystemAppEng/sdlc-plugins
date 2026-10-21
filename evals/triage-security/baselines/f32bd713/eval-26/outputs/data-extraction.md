# Step 1 -- Data Extraction: TC-8050

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99001 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | criterion |
| Affected version range | versions before 0.5.2 |
| Fixed version | 0.5.2 |
| Upstream fix PR | (none found in remote links) |
| Advisory URL | (none found in remote links) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99001 |
| Due date | 2026-08-01 |
| Existing comments | None |
| CVSS | 5.3 (Medium) |

## Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]`, which maps to configured Version Stream **2.2.x** (`git.example.com/rhtpa/rhtpa-release.0.4.z`).

**Issue stream scope**: 2.2.x (scoped -- triage is limited to this stream for Case B remediation; other affected streams are handled via Case A cross-stream impact).

## Ecosystem Detection

**Ecosystem**: Cargo (source dependency)

The vulnerable library `criterion` is a Rust crate. The Cargo ecosystem is configured in the 2.2.x stream's Ecosystem Mappings table with lock file `Cargo.lock` and upstream branch `release/0.4.z`.

**Ecosystem classification**: Source dependency -- produces 2 remediation tasks per stream (upstream backport/dependency bump + downstream propagation).

## Deployment Context

Repository `rhtpa-backend` is listed in Source Repositories with URL `https://github.com/rhtpa/rhtpa-backend`. No Deployment Context column is present in the Source Repositories table, so the default deployment context is **upstream**.
