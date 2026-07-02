# Step 1 -- Data Extraction

## Issue: TC-8030

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-48901 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | "versions prior to the fix" (imprecise -- no exact threshold in Jira description) |
| Fixed version | "see advisory" (imprecise -- no exact version in Jira description) |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 |
| Due date | 2026-08-01 |
| Assignee | Unassigned |
| Status | New |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

The issue is scoped to stream **2.2.x** only.

## Ecosystem Detection

The vulnerable library is **h2**, a Rust crate. The ecosystem is **Cargo**.

From the 2.2.x stream's Ecosystem Mappings:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | Cargo.lock | `git show <tag>:Cargo.lock` | release/0.4.z |

## Deployment Context

The affected repository `rhtpa-backend` is found in the Source Repositories table. No Deployment Context column is present, so the default of `upstream` applies.

## Critical Data Gap

The Jira description does not provide a precise affected version range or fixed version for h2. The description states "versions prior to the fix" and "see advisory" -- these are insufficient for version impact analysis. External CVE data enrichment (Step 1.5) is required to obtain a machine-readable fix threshold.

## Remote Links

| Link | Type |
|------|------|
| [GHSA-2026-r7f2-kk9p](https://github.com/advisories/GHSA-2026-r7f2-kk9p) | GitHub Advisory |
| [CVE-2026-48901](https://www.cve.org/CVERecord?id=CVE-2026-48901) | CVE Record |
| [hyperium/h2#800](https://github.com/hyperium/h2/pull/800) | Upstream fix PR |
