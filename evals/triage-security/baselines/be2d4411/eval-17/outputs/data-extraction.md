# Step 1 -- Data Extraction

## Issue: TC-8001

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 (versions before 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | (none) |

## Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]`, which maps to configured Version Stream **2.2.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

This issue is **scoped** to stream 2.2.x. Steps 3-4 will apply only to versions within this stream.

## Ecosystem Detection

Library `quinn-proto` is a Rust crate. Ecosystem: **Cargo**.

Lock file: `Cargo.lock`
Check command: `git show <tag>:Cargo.lock`
Upstream branch: `release/0.4.z` (for stream 2.2.x)

## Deployment Context

Repository `rhtpa-backend` found in Source Repositories table. No Deployment Context column present (backward compatibility) -- defaulting to `upstream`.
