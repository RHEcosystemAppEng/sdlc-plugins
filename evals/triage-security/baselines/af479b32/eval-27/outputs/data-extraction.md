# Step 1 -- Data Extraction

## Issue: TC-8051

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99002 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | rustls |
| Affected version range | versions before 0.23.5 |
| Fixed version | 0.23.5 |
| CVSS | 8.1 (High) |
| Upstream fix PR | https://github.com/rustls/rustls/pull/2100 |
| Advisory URL | -- |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99002 |
| Due date | 2026-08-01 |
| Existing comments | (no comments) |

## Stream Scope Resolution

Summary suffix `[rhtpa-2.2]` maps to stream **2.2.x** in the Version Streams table.

Issue stream scope: **2.2.x** (Konflux release repo: rhtpa-release.0.4.z)

## Ecosystem Detection

Vulnerable library `rustls` is a Rust crate. Ecosystem: **Cargo**

Lock file: `Cargo.lock`
Check command: `git show <tag>:Cargo.lock`
Upstream branch: `release/0.4.z`

## Deployment Context

Repository `rhtpa-backend` found in Source Repositories table. Deployment context defaults to `upstream` (no Deployment Context column configured).
