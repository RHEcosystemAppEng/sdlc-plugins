# Step 1 -- Data Extraction: TC-8050

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99001 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
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

Summary suffix `[rhtpa-2.2]` maps to stream **2.2.x** in the Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

Issue stream scope: **2.2.x** (scoped -- Steps 2-8 analyze only this stream for Affects Versions and remediation; other streams are checked for cross-stream impact in Case A).

## Ecosystem Detection

Vulnerable library: **criterion** (Rust crate)
Ecosystem: **Cargo**
Category: **Source dependency** (2 remediation tasks per stream: upstream backport + downstream propagation)

Lock file: `Cargo.lock`
Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "criterion"'`
Upstream branch: `release/0.4.z`

## Deployment Context

Repository `rhtpa-backend` has no explicit Deployment Context column in the Source Repositories table. Default: **upstream**.
