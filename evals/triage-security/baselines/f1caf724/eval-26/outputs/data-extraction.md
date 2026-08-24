# Step 1 -- Data Extraction

## Vulnerability Issue: TC-8050

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99001 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | criterion |
| Affected version range | versions before 0.5.2 |
| Fixed version | 0.5.2 |
| CVSS | 5.3 (Medium) |
| Upstream fix PR | (none found in remote links) |
| Advisory URL | (none found in remote links) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99001 |
| Due date | 2026-08-01 |
| Existing comments | (none) |

## Stream Scope Resolution

Issue summary suffix `[rhtpa-2.2]` maps to configured Version Stream **2.2.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`). Triage is scoped to the 2.2.x stream.

## Ecosystem Detection

The vulnerable library `criterion` is a Rust crate. Ecosystem: **Cargo** (source dependency). Per the ecosystem classification table, source dependency ecosystems produce 2 remediation tasks per stream (upstream backport + downstream propagation).

## Deployment Context

Repository `rhtpa-backend` deployment context defaults to `upstream` (Deployment Context column absent from Source Repositories table).
