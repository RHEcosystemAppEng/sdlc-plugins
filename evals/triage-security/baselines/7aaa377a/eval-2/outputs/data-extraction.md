# Step 1 -- Data Extraction

## TC-8002: CVE-2026-28940 serde_json - Stack overflow on deeply nested input [rhtpa-2.2]

### Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-28940 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | serde_json |
| Affected version range | < 1.0.135 |
| Fixed version | 1.0.135 |
| CVSS | 5.3 (Medium) |
| Upstream fix PR | _(none in remote links)_ |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| Due date | 2026-07-30 |
| Existing comments | _(none)_ |

### Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the
**2.2.x** version stream in the Version Streams table of Security Configuration.

- Stream: 2.2.x
- Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.4.z
- Local Path: /home/dev/repos/rhtpa-release.0.4.z

### Ecosystem Detection

The vulnerable library **serde_json** is a Rust crate. Based on the Ecosystem
Mappings table in the 2.2.x stream's security-matrix.md, the ecosystem is
**Cargo**.

- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`

Cargo is a **source dependency** ecosystem, which would normally produce two
remediation tasks per stream (upstream backport + downstream propagation).

### Deployment Context Lookup

The Source Repositories table in Security Configuration does not include a
Deployment Context column. Per backward compatibility rules, all repositories
default to `upstream`.

- Repository: rhtpa-backend
- Deployment Context: upstream (default -- no Deployment Context column present)
