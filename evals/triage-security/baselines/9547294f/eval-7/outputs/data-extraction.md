# Step 1 -- Data Extraction

## Issue: TC-8006

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.1] |
| Affects Versions (Jira field) | RHTPA 2.1.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | (none in remote links) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |

### Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.1]`. This maps to the **2.1.x** stream from the Version Streams table in Security Configuration (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.3.z`).

**Issue stream scope**: 2.1.x (scoped to stream rhtpa-2.1 only)

### Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. Based on the Ecosystem Mappings table in the 2.1.x stream's security-matrix.md, this maps to ecosystem **Cargo** with:
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.3.z`

### Existing Issue Links

The following links already exist on TC-8006:

| Link Type | Direction | Linked Issue |
|-----------|-----------|-------------|
| Related | outward (TC-8006 -> TC-8001) | TC-8001 (CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]) |
