# Step 1 -- Data Extraction

## Parsed CVE Data from TC-8001

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Reporter | psirt-analyst (account ID: 557058:psirt-analyst-mock-id) |
| Existing comments | None |

## Stream Scope Resolution

Issue summary suffix: `[rhtpa-2.2]`
Mapped to configured Version Stream: **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`)

The issue is **scoped** to the 2.2.x stream. Steps 3 and 8 will be scoped to this stream. Cross-stream impact on 2.1.x will be handled via Case A.

## Ecosystem Detection

Vulnerable library: `quinn-proto` (Rust crate)
Detected ecosystem: **Cargo**
Category: Source dependency
Lock file: `Cargo.lock`
Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`

Ecosystem Mappings (from security-matrix.md):

| Stream | Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|--------|-----------|------------|-----------|---------------|-----------------|
| 2.1.x | Cargo | backend | Cargo.lock | `git show <tag>:Cargo.lock` | release/0.3.z |
| 2.2.x | Cargo | backend | Cargo.lock | `git show <tag>:Cargo.lock` | release/0.4.z |

## Deployment Context

Repository `rhtpa-backend` has no explicit Deployment Context column in Security Configuration. Defaulting to: **upstream**.
