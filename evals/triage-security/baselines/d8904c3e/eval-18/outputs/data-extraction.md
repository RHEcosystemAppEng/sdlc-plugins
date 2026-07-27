# Step 1 -- Data Extraction: TC-8001

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x (mapped from summary suffix `[rhtpa-2.2]` to Version Streams table) |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Ecosystem | Cargo (Rust crate) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Status | In Progress |
| Assignee | engineer-a@example.com |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server, ai-cve-triaged |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the `2.2.x` version stream in Security Configuration. This issue is **stream-scoped** to 2.2.x only. The corresponding Konflux release repo is `rhtpa-release.0.4.z`.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The 2.2.x stream's Ecosystem Mappings table lists **Cargo** with lock file `Cargo.lock` and check command `git show <tag>:Cargo.lock`. Cargo is a source dependency ecosystem, so remediation produces **2 tasks per stream** (upstream backport + downstream propagation).

## Version Impact Analysis (from security-matrix.md mock data)

Using the quinn-proto versions by tag from the security matrix:

| Version | Stream | Build Tag | quinn-proto version | Affected? (< 0.11.14) |
|---------|--------|-----------|---------------------|------------------------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES |
| 2.2.2 | 2.2.x | v0.4.9 | (retag of v0.4.8 = 0.11.12) | YES |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO (fixed) |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO (fixed) |

## Existing Comments

1. **Description digest comment**: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2` (posted 2026-07-01T10:00:00Z by sdlc-workflow/triage-security)
2. **Post-triage summary comment**: Documents triage completion, version impact, actions taken (Affects Versions corrected, ai-cve-triaged label added, remediation tasks TC-8100 and TC-8101 created, transitioned to In Progress). Posted 2026-07-01T10:01:00Z by sdlc-workflow/triage-security.

## Existing Issue Links

| Link Type | Linked Issue | Summary | Status |
|-----------|-------------|---------|--------|
| Depend | TC-8100 | Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2] | In Progress |
| Depend | TC-8101 | Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2] | Open |

TC-8101 blocks TC-8100 (downstream propagation blocked by upstream backport).

## Remote Links

| Title | URL |
|-------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
