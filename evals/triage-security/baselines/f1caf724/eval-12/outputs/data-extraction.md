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
| Affected version range | versions prior to the fix (imprecise -- no exact threshold in Jira description) |
| Fixed version | see advisory (imprecise -- no exact version in Jira description) |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 |
| Due date | 2026-08-01 |
| Existing comments | None |
| Status | New |
| Assignee | Unassigned |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration Version Streams table:

| Stream | Konflux Release Repo |
|--------|----------------------|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z |

The issue is **scoped** to the 2.2.x stream. Steps 3-8 will apply within this stream scope, with cross-stream impact analysis for other streams (2.1.x).

## Ecosystem Detection

The vulnerable library `h2` is a Rust crate (Cargo ecosystem). From the 2.2.x stream's Ecosystem Mappings:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

**Ecosystem classification**: Cargo is a source dependency ecosystem, which means remediation produces **2 tasks per stream** (upstream backport + downstream propagation).

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-r7f2-kk9p |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-48901 |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 |

## Data Quality Note

The Jira description provides imprecise version information:
- **Affected versions**: "versions prior to the fix" -- no numeric threshold
- **Fixed version**: "see advisory" -- no explicit version number

External CVE data enrichment (Step 1.5) is required to establish the precise fix threshold for version impact analysis.
